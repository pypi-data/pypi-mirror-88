# -*- coding: utf-8 -*-
# Copyright (C) Joshua Smith (2016-)
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

"""Check if a trigger was vetoed by a specified hveto run
"""

import os
import sys
import json

from gwpy.segments import SegmentList

from gwdetchar import cli

from .. import __version__

__author__ = 'Joshua Smith <joshua.smith@ligo.org>'


# -- parse command line -------------------------------------------------------

def _abs_path(p):
    return os.path.abspath(os.path.expanduser(p))


def create_parser():
    """Create a command-line parser for this entry point
    """
    parser = cli.create_parser(
        description=__doc__,
        version=__version__,
    )
    parser.add_argument(
        '-t',
        '--trigger-time',
        required=True,
        help='GPS time of the trigger',
    )
    parser.add_argument(
        '-d',
        '--directory',
        required=True,
        type=_abs_path,
        help=('path to hveto-generated folder containing '
              'a summary-stats.json file'),
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_const',
        dest='loglevel',
        const='DEBUG',
        default='INFO',
        help='Log verbose output',
    )
    return parser


# -- main code block ----------------------------------------------------------

def main(args=None):
    """Run the trace tool
    """
    parser = create_parser()
    args = parser.parse_args(args=args)
    directory = args.directory

    logger = cli.logger(name='hveto.trace', level=args.loglevel)
    logger.debug('Running in verbose mode')
    logger.debug('Search directory: %s' % directory)

    trigger_time = float(args.trigger_time)
    if directory[-1] != '/':
        directory += '/'

    try:
        segment_stats = json.load(open('%ssummary-stats.json' % directory))
    except IOError:
        logger.error("'summary-stats.json' was not found "
                     "in the input directory")
        sys.exit(0)

    for i, cround in enumerate(segment_stats['rounds']):
        seg_files = filter(
            lambda f_name: '.txt' in f_name, cround[u'files'][u'VETO_SEGS'])
        for f in seg_files:
            segments = SegmentList.read(os.path.join(directory, f))
            for segment in segments:
                if segment[0] <= trigger_time <= segment[1]:
                    logger.info('Signal was vetoed in round %d by '
                                'segment %s' % ((i + 1), segment))
                    logger.debug('Winner: %s' % cround['name'])
                    logger.debug('Significance: %s' % cround['significance'])
                    logger.debug('SNR: %s' % cround['snr'])
                    logger.debug('Window: %s' % cround['window'])
                    sys.exit(0)

    logger.info('Signal was not vetoed.')


if __name__ == "__main__":
    main()
