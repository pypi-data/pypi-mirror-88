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


import os
from tsquery.cli import cli
if os.getenv('TSQUERY_DEBUG'):
    import logging
    from tsquery import logger
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
cli()
