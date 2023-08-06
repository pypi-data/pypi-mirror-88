# -*- coding: utf-8 -*-
# Copyright (C) Joshua Smith (2016)
#
# This file is part of the hveto python package.
#
# hveto is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hveto is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with hveto.  If not, see <http://www.gnu.org/licenses/>.

"""Create a (temporary) cache of event triggers for analysis by `hveto`

This method will apply the minimal SNR thresholds and any frequency cuts
as given in the configuration files
"""

import h5py
import os
import multiprocessing
import sys
import warnings

from pathlib import Path

from astropy.table import vstack

from gwpy.io.cache import (
    cache_segments,
    file_segment,
    read_cache,
)
from gwpy.segments import (
    Segment,
    SegmentList,
    DataQualityFlag,
    DataQualityDict,
)

from gwdetchar import cli

from .. import (__version__, config)
from ..triggers import (
    get_triggers,
    find_auxiliary_channels,
    find_trigger_files,
)
from ..utils import write_lal_cache

__author__ = 'Duncan Macleod <duncan.macleod@ligo.org>'

IFO = os.getenv('IFO')

# set up logger
PROG = ('python -m hveto.cli.cache_events' if sys.argv[0].endswith('.py')
        else os.path.basename(sys.argv[0]))
LOGGER = cli.logger(name=PROG.split('python -m ').pop())


# -- parse command line -------------------------------------------------------

def _abs_path(p):
    return Path(p).expanduser().resolve()


def create_parser():
    """Create a command-line parser for this entry point
    """
    parser = cli.create_parser(
        prog=PROG,
        description=__doc__,
        version=__version__,
    )

    # gwdetchar standard arguments/options
    cli.add_gps_start_stop_arguments(parser)
    cli.add_ifo_option(parser, required=IFO is None, ifo=IFO)
    cli.add_nproc_option(parser, default=1)

    # custom options
    parser.add_argument(
        '-f',
        '--config-file',
        action='append',
        default=[],
        type=_abs_path,
        help=('path to hveto configuration file, can be given '
              'multiple times (files read in order)'),
    )
    parser.add_argument(
        '-p',
        '--primary-cache',
        default=None,
        type=_abs_path,
        help='path for cache containing primary channel files',
    )
    parser.add_argument(
        '-a',
        '--auxiliary-cache',
        default=None,
        type=_abs_path,
        help=('path for cache containing auxiliary channel files, '
              'files contained must be T050017-compliant with the '
              'channel name as the leading name parts, e.g. '
              '\'L1-GDS_CALIB_STRAIN_<tag>-<start>-<duration>.'
              '<ext>\' for L1:GDS-CALIB_STRAIN triggers'),
    )
    parser.add_argument(
        '-S',
        '--analysis-segments',
        action='append',
        default=[],
        type=_abs_path,
        help=('path to LIGO_LW XML file containing segments for '
              'the analysis flag (name in segment_definer table '
              'must match analysis-flag in config file)'),
    )
    parser.add_argument(
        '--append',
        action='store_true',
        default=False,
        help=('append to existing cached event files, otherwise, '
              'start from scratch (default)'),
    )

    # output options
    pout = parser.add_argument_group('Output options')
    pout.add_argument(
        '-o',
        '--output-directory',
        default=os.curdir,
        type=_abs_path,
        help='path of output directory, default: %(default)s',
    )

    # return the parser
    return parser


# -- main code block ----------------------------------------------------------

def main(args=None):
    """Run the cache_events tool
    """
    parser = create_parser()
    args = parser.parse_args(args=args)

    ifo = args.ifo
    start = int(args.gpsstart)
    end = int(args.gpsend)
    duration = end - start

    LOGGER.info("-- Welcome to Hveto --")
    LOGGER.info("GPS start time: %d" % start)
    LOGGER.info("GPS end time: %d" % end)
    LOGGER.info("Interferometer: %s" % ifo)

    # -- initialisation -------------------------------

    # read configuration
    cp = config.HvetoConfigParser(ifo=args.ifo)
    cp.read(map(str, args.config_file))
    LOGGER.info("Parsed configuration file(s)")

    # format output directory
    outdir = args.output_directory
    outdir.mkdir(parents=True, exist_ok=True)
    LOGGER.info("Working directory: {}".format(outdir))
    trigdir = outdir / 'triggers'
    trigdir.mkdir(parents=True, exist_ok=True)

    # get segments
    aflag = cp.get('segments', 'analysis-flag')
    url = cp.get('segments', 'url')
    padding = cp.getfloats('segments', 'padding')
    if args.analysis_segments:
        segs_ = DataQualityDict.read(args.analysis_segments, gpstype=float)
        analysis = segs_[aflag]
        span = SegmentList([Segment(start, end)])
        analysis.active &= span
        analysis.known &= span
        analysis.coalesce()
        LOGGER.debug("Segments read from disk")
    else:
        analysis = DataQualityFlag.query(aflag, start, end, url=url)
        LOGGER.debug("Segments recovered from %s" % url)
    analysis.pad(*padding)
    livetime = int(abs(analysis.active))
    livetimepc = livetime / duration * 100.
    LOGGER.info("Retrieved %d segments for %s with %ss (%.2f%%) livetime"
                % (len(analysis.active), aflag, livetime, livetimepc))

    snrs = cp.getfloats('hveto', 'snr-thresholds')
    minsnr = min(snrs)

    # -- utility methods ------------------------------

    def create_path(channel):
        ifo, name = channel.split(':', 1)
        name = name.replace('-', '_')
        return trigdir / "{}-{}-{}-{}.h5".format(ifo, name, start, duration)

    def read_and_cache_events(channel, etg, cache=None, trigfind_kw={},
                              **read_kw):
        cfile = create_path(channel)
        # read existing cached triggers and work out new segments to query
        if args.append and cfile.is_file():
            previous = DataQualityFlag.read(
                str(cfile),
                path='segments',
                format='hdf5',
            ).coalesce()
            new = analysis - previous
        else:
            new = analysis.copy()
        # get cache of files
        if cache is None:
            cache = find_trigger_files(channel, etg, new.active, **trigfind_kw)
        else:
            cache = list(filter(
                lambda e: new.active.intersects_segment(file_segment(e)),
                cache,
            ))
        # restrict 'active' segments to when we have data
        try:
            new.active &= cache_segments(cache)
        except IndexError:
            new.active = type(new.active)()
        # find new triggers
        try:
            trigs = get_triggers(channel, etg, new.active, cache=cache,
                                 raw=True, **read_kw)
        # catch error and continue
        except ValueError as e:
            warnings.warn('%s: %s' % (type(e).__name__, str(e)))
        else:
            path = write_events(channel, trigs, new)
            try:
                return path, len(trigs)
            except TypeError:  # None
                return

    def write_events(channel, tab, segments):
        """Write events to file with a given filename
        """
        # get filename
        path = create_path(channel)
        h5f = h5py.File(str(path), 'a')

        # read existing table from file
        try:
            old = tab.read(h5f["triggers"], format="hdf5")
        except KeyError:
            pass
        else:
            tab = vstack(old, tab)

        # append event table
        tab.write(h5f, path="triggers", append=True, overwrite=True)

        # write segments
        try:
            oldsegs = DataQualityFlag.read(h5f, path="segments", format="hdf5")
        except KeyError:
            pass
        else:
            segments = oldsegs + segments
        segments.write(h5f, path="segments", append=True, overwrite=True)

        # write file to disk
        h5f.close()
        return path

    # -- load channels --------------------------------

    # get primary channel name
    pchannel = cp.get('primary', 'channel')

    # read auxiliary cache
    if args.auxiliary_cache is not None:
        acache = [e for c in args.auxiliary_cache for e in read_cache(str(c))]
    else:
        acache = None

    # load auxiliary channels
    auxetg = cp.get('auxiliary', 'trigger-generator')
    auxfreq = cp.getfloats('auxiliary', 'frequency-range')
    try:
        auxchannels = cp.get('auxiliary', 'channels').strip('\n').split('\n')
    except config.configparser.NoOptionError:
        auxchannels = find_auxiliary_channels(auxetg, start, ifo=args.ifo,
                                              cache=acache)

    # load unsafe channels list
    _unsafe = cp.get('safety', 'unsafe-channels')
    if os.path.isfile(_unsafe):  # from file
        unsafe = set()
        with open(_unsafe, 'rb') as f:
            for c in f.read().rstrip('\n').split('\n'):
                if c.startswith('%(IFO)s'):
                    unsafe.add(c.replace('%(IFO)s', ifo))
                elif not c.startswith('%s:' % ifo):
                    unsafe.add('%s:%s' % (ifo, c))
                else:
                    unsafe.add(c)
    else:  # or from line-seprated list
        unsafe = set(_unsafe.strip('\n').split('\n'))
    unsafe.add(pchannel)
    cp.set('safety', 'unsafe-channels', '\n'.join(sorted(unsafe)))
    LOGGER.debug("Read list of %d unsafe channels" % len(unsafe))

    # remove duplicates
    auxchannels = sorted(set(auxchannels))
    LOGGER.debug("Read list of %d auxiliary channels" % len(auxchannels))

    # remove unsafe channels
    nunsafe = 0
    for i in range(len(auxchannels) - 1, -1, -1):
        if auxchannels[i] in unsafe:
            LOGGER.warning("Auxiliary channel %r identified as unsafe and has "
                           "been removed" % auxchannels[i])
            auxchannels.pop(i)
            nunsafe += 1
    LOGGER.debug("%d auxiliary channels identified as unsafe" % nunsafe)
    naux = len(auxchannels)
    LOGGER.info("Identified %d auxiliary channels to process" % naux)

    # -- load primary triggers -------------------------

    LOGGER.info("Reading events for primary channel...")

    # read primary cache
    if args.primary_cache is not None:
        pcache = [e for c in args.primary_cache for e in read_cache(str(c))]
    else:
        pcache = None

    # get primary params
    petg = cp.get('primary', 'trigger-generator')
    psnr = cp.getfloat('primary', 'snr-threshold')
    pfreq = cp.getfloats('primary', 'frequency-range')
    preadkw = cp.getparams('primary', 'read-')
    ptrigfindkw = cp.getparams('primary', 'trigfind-')

    # load primary triggers
    out = read_and_cache_events(pchannel, petg, snr=psnr, frange=pfreq,
                                cache=pcache, trigfind_kw=ptrigfindkw,
                                **preadkw)
    try:
        e, n = out
    except TypeError:
        e = None
        n = 0
    if n:
        LOGGER.info("Cached %d new events for %s" % (n, pchannel))
    elif args.append and e.is_file():
        LOGGER.info("Cached 0 new events for %s" % pchannel)
    else:
        message = "No events found for %r in %d seconds of livetime" % (
           pchannel, livetime)
        LOGGER.critical(message)

    # write primary to local cache
    pname = trigdir / '{}-HVETO_PRIMARY_CACHE-{}-{}.lcf'.format(
        ifo, start, duration,
    )
    write_lal_cache(str(pname), [e])
    LOGGER.info('Primary cache written to {}'.format(pname))

    # -- load auxiliary triggers -----------------------

    LOGGER.info("Reading triggers for aux channels...")
    counter = multiprocessing.Value('i', 0)

    areadkw = cp.getparams('auxiliary', 'read-')
    atrigfindkw = cp.getparams('auxiliary', 'trigfind-')

    def read_and_write_aux_triggers(channel):
        if acache is None:
            auxcache = None
        else:
            ifo, name = channel.split(':')
            match = "{}-{}".format(ifo, name.replace('-', '_'))
            auxcache = [e for e in acache if Path(e).name.startswith(match)]

        out = read_and_cache_events(
            channel, auxetg, cache=auxcache, snr=minsnr, frange=auxfreq,
            trigfind_kw=atrigfindkw, **areadkw)
        try:
            e, n = out
        except TypeError:
            e = None
            n = 0
        # log result of load
        with counter.get_lock():
            counter.value += 1
            tag = '[%d/%d]' % (counter.value, naux)
            if e is None:  # something went wrong
                LOGGER.critical("    %s Failed to read events for %s"
                                % (tag, channel))
            else:  # either read events or nothing new
                LOGGER.debug("    %s Cached %d new events for %s"
                             % (tag, n, channel))
        return e

    # map with multiprocessing
    if args.nproc > 1:
        pool = multiprocessing.Pool(processes=args.nproc)
        results = pool.map(read_and_write_aux_triggers, auxchannels)
        pool.close()
    # map without multiprocessing
    else:
        results = map(read_and_write_aux_triggers, auxchannels)

    acache = [x for x in results if x is not None]
    aname = trigdir / '{}-HVETO_AUXILIARY_CACHE-{}-{}.lcf'.format(
        ifo, start, duration,
    )
    write_lal_cache(str(aname), acache)
    LOGGER.info('Auxiliary cache written to {}'.format(aname))

    # -- finish ----------------------------------------

    LOGGER.info('Done, you can use these cache files in an hveto analysis by '
                'passing the following arguments:\n\n--primary-cache {} '
                '--auxiliary-cache {}\n'.format(pname, aname))


# -- run code -----------------------------------------------------------------

if __name__ == "__main__":
    main()
