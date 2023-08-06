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
Classes
'''


from sys import stdout
from typing import Any, TypeVar
from colorama import Fore, Style


InfoHandle = TypeVar("InfoHandle", str, int)


AVAIL_GLOSS = [Style.RESET_ALL, Style.NORMAL, Style.DIM, Style.BRIGHT]
AVAIL_COLORS = [Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
                Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
                Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
                Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
                Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX]


class InfoMark():
    '''
    Information object
    '''
    def __init__(self, pref_long_str: str = '',
                 pref_short_str: str = '>', **kwargs) -> None:
        '''
        pref_long_str: Message-description prefix
        pref_short_str: Short-description (1 character-long)
        pref_color: prefix color (the 16 standard terminal colors)
        pref_gloss: prefix gloss (dim/bright)
        text_color: Out-Text color
        text_gloss: Out-Text gloss

        Initiate object
        '''
        def_args = {'pref_color': 7, 'pref_gloss': 1,
                    'text_color': 7, 'text_gloss': 1}
        kwargs = {**def_args, **kwargs}

        # Standards check
        if not 0 <= len(pref_long_str) <= 10:
            raise ValueError(f"Too long (>10) prefix string '{pref_long_str}'")

        if not 0 <= len(pref_short_str) <= 1:
            raise ValueError(
                f"Short-prefix '{self.short_prefix_str}' must be 1 character"
            )
        if not 0 <= kwargs['text_color'] <= 15:
            print("[WARN] 0 <= color <= 15, using 7")
            kwargs['text_color'] = 7
        if not 0 <= kwargs['pref_color'] <= 15:
            print("[WARN] 0 <= color <= 15, using 7")
            kwargs['pref_color'] = 7
        if not 0 <= kwargs['text_gloss'] <= 3:
            print("[WARN] 0 <= gloss <= 3, using 1")
            kwargs['text_gloss'] = 1
        if not 0 <= kwargs['pref_gloss'] <= 3:
            print("[WARN] 0 <= gloss <= 3, using 1")
            kwargs['pref_gloss'] = 1

        # Styles
        self.pref_long_str: str = pref_long_str.upper()
        self.pref_short_str: str = pref_short_str
        self.pref_color: int = AVAIL_COLORS[kwargs['pref_color']]
        self.text_color: int = AVAIL_COLORS[kwargs['text_color']]
        self.pref_gloss: int = AVAIL_GLOSS[kwargs['pref_gloss']]
        self.text_gloss: int = AVAIL_GLOSS[kwargs['text_gloss']]

    def __str__(self) -> str:
        '''
        string format of available information
        '''
        outstr = AVAIL_GLOSS[0] + '\tshort\tlong\ttext\n'
        outstr += AVAIL_GLOSS[0] + 'prefix:\t{}{}{}\t{}\t{}{}{}\n'.format(
            str(self.pref_color), str(self.pref_gloss),
            self.pref_short_str, self.pref_long_str,
            str(self.text_color), str(self.text_gloss),
            "<CUSTOM>" + AVAIL_GLOSS[0]
        )
        return outstr

    def get_info(self) -> str:
        '''
        This is defined only because flake8 complains that the object has
        only 1 public method

        print information
        '''
        print(str(self))
        return str(self)


class InfoPrint():
    '''
    Fancy Print class that also prints the type of message
    '''
    def __init__(self) -> None:
        '''
        initialize print styles
        '''
        # Standard info styles
        self.info_style = {
            'cont': InfoMark(pref_long_str="", pref_short_str=''),
            'info': InfoMark(pref_long_str="inform",
                             pref_short_str='i', pref_color=2),
            'act': InfoMark(pref_long_str="action",
                            pref_short_str='@', pref_color=3),
            'list': InfoMark(pref_long_str="list",
                             pref_short_str='·', pref_color=4),
            'warn': InfoMark(pref_long_str="warning",
                             pref_short_str='?', pref_color=5),
            'err': InfoMark(pref_long_str="error", pref_short_str='!',
                            pref_color=1, pref_gloss=1, text_color=1,
                            text_gloss=2),
            'bug': InfoMark(pref_long_str="debug", pref_short_str='#',
                            pref_color=6, text_color=6, text_gloss=2),
        }
        self.max_info_size = 7
        self.info_index = ['cont', 'info', 'act', 'list', 'warn', 'err', 'bug']
        self.switches = {'pad': False, 'short': False,
                         'bland': False, 'disabled': False}
        self.mark_kwargs = {'text_color': 7, 'text_gloss': 1,
                            'pref_color': 7, 'pref_gloss': 1, }
        self.print_kwargs = {'file': stdout, 'sep': "\t",
                             'end': "\n", 'flush': False}

    def __str__(self) -> str:
        '''
        formatted InfoPrint().info_style
        '''
        return "\n".join((f"{k}:{v}" for k, v in self.info_style.items()))

    def _prefix_mark(self, mark: InfoMark = None,
                     index_str: InfoHandle = 0, **kwargs) -> str:
        '''
        mark: passed info mark
        index_str: string to call info
        short: info_mark is in short form
        pad: Pad info mark
        bland: colorless info mark
        disabled: Default python print function-like behaviour
        standard prefixed string
        '''
        kwargs = {**self.switches, **kwargs}
        if mark is None:
            if isinstance(index_str, int):
                if not 0 <= index_str < len(self.info_index):
                    index_str = 0
                mark = self.info_style[self.info_index[index_str]]
            elif isinstance(index_str, str):
                mark = self.info_style.get(index_str, self.info_style['cont'])
            else:
                raise TypeError(f"{index_str} should be either str or int")
        info = mark.pref_short_str if kwargs['short'] else mark.pref_long_str
        if kwargs['bland']:
            # Colorless output
            return self._prefix(info, short=kwargs['short'], pad=kwargs['pad'])
        return mark.pref_color + mark.pref_gloss + self._prefix(
            info, short=kwargs['short'], pad=kwargs['pad']
        ) + mark.text_color + mark.text_gloss

    def _prefix(self, info, short: bool = None, pad: bool = None) -> str:
        '''
        prepend spaces and [ ] to make it pretty
        '''
        if short is None:
            short = self.switches['short']
        if pad is None:
            pad = self.switches['pad']
        infolen = len(info)
        if not info:
            infolen = - 2
        pad_len = 1 - infolen if short else self.max_info_size - infolen
        if pad_len < 0:
            pad_len = 0
        prefix = f"[{info}]" if info else ""
        padstr = " " + " " * pad_len
        return prefix + padstr * pad

    def psprint(self, *args, pref: InfoHandle = None, **kwargs) -> None:
        '''
        *args: passed on to print_function for printing
        pref: str/int: pre-declared InfoMark defaults: {
        cont: or 0 or anything else
        info: or 1
        act:  or 2
        list: or 3
        warn: or 4
        error:or 5
        bug:  or 6 } OR in **kwargs {
        pref_color: int (7)
        pref_gloss: int (1)
        text_color: int (7)
        text_gloss: int (1)
        pref_long_str:  ">" }
        pad: if true, print with padding after pref
        short: if true, use {pref_short_str} instead
        bland: colorless
        disabled: behave like print_function

        everyting else is passed to print_function
        '''
        if not args:
            print()
            return

        # Extract keys
        print_kwargs = {}
        for key, default in self.print_kwargs.items():
            print_kwargs[key] = kwargs[key] if key in kwargs else default

        switches = {}
        for key, default in self.switches.items():
            switches[key] = kwargs[key] if key in kwargs else default
        if switches['disabled']:
            print(*args, **print_kwargs)
            return

        mark_kwargs = {}
        for key, default in self.mark_kwargs.items():
            mark_kwargs[key] = kwargs[key] if key in kwargs else default
        for key in 'pref_long_str', 'pref_short_str':
            mark_kwargs[key] = kwargs[key] if key in kwargs else ''

        if pref is None:
            on_the_fly = InfoMark(**mark_kwargs)
        else:
            on_the_fly = None
        args = list(args)
        args[0] = self._prefix_mark(mark=on_the_fly, index_str=pref,
                                    **switches) + str(args[0])
        args[-1] = str(args[-1]) + AVAIL_GLOSS[0]
        print(*args, **print_kwargs)

    def edit_style(self, pref_long_str, index_handle: int = None,
                   index_str: str = None, **kwargs) -> str:
        '''
        index: Index handle that will call this InfoMark
        index_str: Index string handle that will call this InfoMark
        color: terminal color indices [0 - 15]
        gloss: Bright/Dim
        **kwargs: passed to InfoMark for initialization

        Orders:
        colors: 0:BLACK\t1:RED\t2:GREEN\t3:YELLOW
                4:BLUE\t5:MAGENTA\t6:CYAN\t7:WHITE
                    and their Dim/Bright versions
        styles: 0:RESET_ALL\t1:NORMAL\t2:DIM\t3:BRIGHT

        returns the new (updated) info_style
        '''
        if index_handle is None or \
           not 0 <= index_handle <= len(self.info_index):
            self.info_index.append(index_str)
        else:
            self.info_index.insert(index_handle, index_str)
        self.info_style[index_str] = InfoMark(pref_long_str=pref_long_str,
                                              **kwargs)
        return str(self)

    def remove_style(self, index_str: str = None,
                     index_handle: int = None) -> str:
        '''
        index_str: is popped out of defined styles
        index_handle: is used to locate index_str if it is not provided

        returns the new (updated) info_style
        '''
        if index_str is None:
            if index_handle < len(self.info_style):
                index_str = self.info_index.pop(index_handle)
        del self.info_style[index_str]
        return str(self)
