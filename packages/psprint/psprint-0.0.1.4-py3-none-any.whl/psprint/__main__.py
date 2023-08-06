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
module init
'''


from . import PRINT as print


if __name__ in ("__main__", "psprint.__main__"):
    print()
    print("usage:",
          pref='err', pad=True, short=False)
    print("Use me as an imported module",
          pref='info', pad=True, short=False)
    print("from psprint import PRINT as print",
          pref='act', pad=True, short=False)
    print("Styles may be edited by importing the InfoPrint class",
          pref='list', pad=True, short=False)
    print("Or by editing its DEFAULT_PRINT instance",
          pad=True, short=False)
    print("Bye",
          pref='bug', pad=True, short=False)
    print()
