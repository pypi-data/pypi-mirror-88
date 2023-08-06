# Copyright Greg Werbin, 2020
#
# This file is part of TSQuery.
#
# TSQuery is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# TSQuery is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TSQuery.  If not, see <https://www.gnu.org/licenses/>.


import logging
logger = logging.getLogger(__name__)

# TODO:
#  * Implement `tsview` which presents the available patterns (and their fields, if any) for the given language (should probably use Node and not Python)
#  * Implement `tsbuild` which builds .so from C source (using Python API `Language.build`)
#  * Refactor cli.py so that both tsbuild and tsquery are supported
