# -*- coding: utf-8 -*-
# Copyright (C) Louisiana State University (2013)
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

"""Setup the Hveto package
"""

from setuptools import setup

import versioneer

# versioneer
version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()

# import sphinx commands
try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    pass
else:
    cmdclass['build_sphinx'] = BuildDoc

# run setup
# NOTE: all other metadata and options come from setup.cfg
setup(
    version=version,
    cmdclass=cmdclass,
)
