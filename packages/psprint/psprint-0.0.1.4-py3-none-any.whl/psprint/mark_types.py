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
Information Marker
'''

from typing import TypeVar
from warnings import warn
from colorama import Fore, Back, Style
from .warn_types import KeyWarning, ValueWarning
from .text_types import PrintPref, PrintText


StrInt = TypeVar("StrInt", str, int)
DEFAULT_STYLE = {'color': 7, 'gloss': 1, 'bgcol': 0}
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


class InfoMark():
    '''
    Information object
    '''
    def __init__(self, parent=None, pref_long_str: str = '',
                 pref_short_str: str = '>', text_args: dict = {},
                 pref_args: dict = {},) -> None:
        '''
        pref_long_str: Message-description prefix
        pref_short_str: Short-description (1 character-long)
        pref_args: dict with keys: color, gloss, bgcol
        text_args: dict with keys: color, gloss, bgcol

        Initiate object
        '''
        # Standards check
        if len(pref_long_str) > 10:
            warn(f"Too long (>10) prefix string '{pref_long_str}', trimming",
                 category=ValueWarning)
            pref_long_str = pref_long_str[:10]

        if len(pref_short_str) > 1:
            warn("Short-prefix must be 1 character, trimming",
                 category=ValueWarning)

        # inheritance:
        if parent is not None:
            if pref_short_str == ">":
                pref_short_str = parent.pref.short
            pref_long_str = pref_long_str or str(parent.pref)
            self.text_args = {**parent.text_args, **text_args}
            self.pref_args = {**parent.pref_args, **pref_args}

        else:
            self.text_args = {**DEFAULT_STYLE, **text_args}
            self.pref_args = {**DEFAULT_STYLE, **pref_args}

        # Styles
        self.pref = PrintPref(val=pref_long_str, short=pref_short_str)
        self.text = PrintText()

        # Settings
        self.pref.color = self._color_idx_2_obj(self.pref_args['color'])
        self.pref.bgcol = self._color_idx_2_obj(self.pref_args['bgcol'],
                                                back=True)
        self.pref.gloss = self._gloss_idx_2_obj(self.pref_args['gloss'])
        self.text.color = self._color_idx_2_obj(self.text_args['color'])
        self.text.bgcol = self._color_idx_2_obj(self.text_args['bgcol'],
                                                back=True)
        self.text.gloss = self._gloss_idx_2_obj(self.text_args['gloss'])

    def _color_idx_2_obj(self, color: StrInt = 7, back=False) -> str:
        '''
        convert color strings to corresponding integers
        '''
        if isinstance(color, int):
            if not 0 <= color <= 15:
                warn("0 <= color <= 15, using 7", category=KeyWarning)
                color = 7
        else:
            for idx, alias_tup in enumerate(
                    (
                        ('k',  '0',  'black'),
                        ('r',  '1',  'red'),
                        ('g',  '2',  'green'),
                        ('y',  '3',  'yellow'),
                        ('b',  '4',  'blue'),
                        ('m',  '5',  'magenta'),
                        ('c',  '6',  'cyan'),
                        ('w',  '7',  'white'),
                        ('lk', '8',  'light black'),
                        ('lr', '9',  'light red'),
                        ('lg', '10', 'light green'),
                        ('ly', '11', 'light yellow'),
                        ('lb', '12', 'light blue'),
                        ('lm', '13', 'light magenta'),
                        ('lc', '14', 'light ctan'),
                        ('lw', '15', 'light white'),
                    )
            ):
                if color in alias_tup:
                    color = idx
                    break
        if not isinstance(color, int):
            warn("Color string was not understood, fallback to default",
                 category=KeyWarning)
            color = 0 if back else 7
        return BACK_COLORS[color] if back else FORE_COLORS[color]

    def _gloss_idx_2_obj(self, gloss: StrInt = 1) -> str:
        '''
        convert gloss strings to corresponding integers
        '''
        if isinstance(gloss, int):
            if not 0 <= gloss <= 3:
                warn("0 <= gloss <= 3, using 1", category=KeyWarning)
                gloss = 1
        else:
            for idx, alias_tup in enumerate(
                    (
                        ('r',  '0',  'reset'),
                        ('n',  '1',  'normal'),
                        ('d',  '2',  'dim'),
                        ('b',  '3',  'bright'),
                    )
            ):
                if gloss in alias_tup:
                    gloss = idx
        if not isinstance(gloss, int):
            warn("Gloss string was not understood, defaulting to normal",
                 category=KeyWarning)
            gloss = 1
        return AVAIL_GLOSS[gloss]

    def __str__(self) -> str:
        '''
        string format of available information
        '''
        return '\t{}\t{}\t{}'.format(self.pref.effects + self.pref.short,
                                     self.pref,
                                     self.text.effects + "<CUSTOM>"
                                     + Style.RESET_ALL)

    def __copy__(self):
        '''
        copy of instance
        '''
        child = InfoMark(pref_long_str=self.pref_long_str,
                         pref_short_str=self.pref_short_str)
        child.pref = self.pref.__copy__()
        child.text = self.text.__copy__()
        return child

    def get_info(self) -> str:
        '''
        This is defined only because flake8 complains that the object has
        only 1 public method

        print information
        '''
        print(str(self))
        return str(self)
