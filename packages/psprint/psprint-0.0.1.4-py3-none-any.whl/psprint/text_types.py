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
Text Parts
'''


from colorama import Fore, Back, Style


AVAIL_GLOSS = [Style.RESET_ALL, Style.NORMAL, Style.DIM, Style.BRIGHT]
FORE_COLORS = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
               Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
               Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
               Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
               Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]
BACK_COLORS = [Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW,
               Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE,
               Back.LIGHTBLACK_EX, Back.LIGHTRED_EX, Back.LIGHTGREEN_EX,
               Back.LIGHTYELLOW_EX, Back.LIGHTBLUE_EX, Back.LIGHTMAGENTA_EX,
               Back.LIGHTCYAN_EX, Back.LIGHTWHITE_EX]


class PrintText():
    '''
    Text to be printed to (ANSI) terminal
    '''
    def __init__(self, val='', color=Fore.WHITE,
                 gloss=Style.NORMAL, bgcol=Back.BLACK) -> None:
        '''
        Plain text object
        '''
        self.val = str(val)
        self.color = color
        self.gloss = gloss
        self.bgcol = bgcol

    @property
    def effects(self) -> str:
        '''
        All effects combined
        '''
        return self.color + self.bgcol + self.gloss

    @effects.setter
    def effects(self, val) -> None:
        '''
        hard set effects
        '''
        self.color = ''
        self.gloss = ''
        self.bgcol = ''
        self.effects = val

    @effects.deleter
    def effects(self) -> None:
        '''
        return all effects as a single string
        '''
        self.color = ''
        self.gloss = ''
        self.bgcol = ''

    def __str__(self) -> str:
        '''
        print self
        '''
        return str(self.val)

    def __len__(self) -> int:
        '''
        length of value
        '''
        return len(self.val)

    def __copy__(self):
        '''
        create a copy
        '''
        return PrintText(val=self.val, color=self.color,
                         gloss=self.gloss, bgcol=self.bgcol)


class PrintPref(PrintText):
    '''
    Prefix that informs about Text
    '''
    def __init__(self, val='', short='>', **kwargs) -> None:
        PrintText.__init__(self, val=val.upper(), **kwargs)
        self.short = short

    def __copy__(self):
        '''
        create a copy
        '''
        return PrintPref(val=self.val, short=self.short,
                         color=self.color, gloss=self.gloss, bgcol=self.bgcol)
