#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020 Pradyumna Paranjape
# This file is part of psprint.
#
# psprint is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# psprint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with psprint.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Prompt String-like Print
'''


import os
import sys
from pathlib import Path
from configparser import ConfigParser
from .printer import InfoPrint


DEFAULT_PRINT = InfoPrint()


RC_LOCATIONS = {
    'root': Path("/etc/psprint/style.conf"),
    'user': Path(os.environ["HOME"]).joinpath("." + "psprintrc"),
    'config': Path(os.environ["HOME"]).joinpath(
        ".config", "psprint", "style.conf"
    ),
    'xdg_config': Path().joinpath("psprintrc"),  # juvenile user|fails
    'local': Path(os.getcwd()).joinpath("." + "psprintrc"),
}

try:
    RC_LOCATIONS['xdg_config'] = Path(
        os.environ["XDG_CONFIG_HOME"]
    ).joinpath("psprint", "style.conf")
except KeyError:
    pass


for loc in 'root', 'user', 'config', 'xdg_config', 'local':
    if RC_LOCATIONS[loc].exists():
        DEFAULT_PRINT.set_opts(RC_LOCATIONS[loc])

if 'idlelib.run' in sys.modules or not sys.stdout.isatty():
    # Running inside idle
    DEFAULT_PRINT.switches['bland'] = True


PRINT = DEFAULT_PRINT.psprint
__all__ = ['InfoPrint', 'DEFAULT_PRINT', 'PRINT']
