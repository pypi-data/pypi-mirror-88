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


from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal


logger = logging.getLogger(__name__)


# TODO: switch from "XDG_CONFIG_HOME" to "config"


_XDG_HOME_T = Literal['XDG_CONFIG_HOME', 'XDG_DATA_HOME']
_XDG_DIRS_T = Literal['XDG_CONFIG_DIRS', 'XDG_DATA_DIRS']


def get_xdg_home(key: _XDG_HOME_T) -> Path:
    """ Implement XDG Base Directory Specification
    See: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """
    if key == 'XDG_CONFIG_HOME':
        default = Path.home() / '.config'
    elif key == 'XDG_DATA_HOME':
        default = default = Path.home() / '.local/share'
    else:
        raise ValueError(f'Unrecognized XDG directory: {key}')

    xdg_path = Path(os.getenv(key, default))
    logger.debug('%s -> %s', key, xdg_path)
    return xdg_path


def get_xdg_dirs(key: _XDG_DIRS_T) -> tuple[Path, ...]:
    """ Implement XDG Base Directory Specification
    See: https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    """
    if key == 'XDG_CONFIG_DIRS':
        default = (Path('/etc/xdg'),)
    elif key == 'XDG_DATA_DIRS':
        default = (Path('/usr/share'), Path('/usr/local/share'))
    else:
        raise ValueError(f'Unrecognized XDG directory: {key}')

    env_val = os.getenv(key)
    if env_val is None:
        paths = default
    else:
        paths = tuple(map(Path, env_val.split(':')))
    logger.debug('%s -> %s', key, ' : '.join(map(str, paths)))
    return paths
