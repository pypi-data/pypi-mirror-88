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
Information- Prepended Print object
'''

from sys import stdout
from configparser import ConfigParser
from colorama import Style
from .mark_types import InfoMark, DEFAULT_STYLE, StrInt


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
            'info': InfoMark(pref_long_str="inform", pref_short_str='i',
                             pref_args={'color': 2}),
            'act': InfoMark(pref_long_str="action", pref_short_str='@',
                            pref_args={'color': 3}),
            'list': InfoMark(pref_long_str="list", pref_short_str='·',
                             pref_args={'color': 4}),
            'warn': InfoMark(pref_long_str="warning", pref_short_str='*',
                             pref_args={'color': 5}),
            'err': InfoMark(pref_long_str="error", pref_short_str='!',
                            pref_args={'color': 1, 'gloss': 3},
                            text_args={'color': 1, 'gloss': 2}),
            'bug': InfoMark(pref_long_str="debug", pref_short_str='#',
                            pref_args={'color': 6},
                            text_args={'color': 6, 'gloss': 2}),
        }
        self.max_info_size = 7
        self.info_index = ['cont', 'info', 'act', 'list', 'warn', 'err', 'bug']
        self.switches = {'pad': False, 'short': False,
                         'bland': False, 'disabled': False}
        self.print_kwargs = {'file': stdout, 'sep': "\t",
                             'end': "\n", 'flush': False}

    def __str__(self) -> str:
        '''
        formatted InfoPrint().info_style
        '''
        outstr = '\npref\tshort\tlong\ttext\n\n'
        outstr += "\n".join((f"{k}:{v}" for k, v in self.info_style.items()))
        return outstr

    def _prefix_mark(self, mark: InfoMark, **switches) -> str:
        '''
        mark: passed info mark
        index_str: string to call pref
        short: info_mark is in short form
        pad: Pad prefix
        bland: colorless pref
        disabled: Default python print function-like behaviour
        standard prefixed string
        '''
        pref: str = mark.pref.short if switches['short'] else mark.pref
        pref_out = self._prefix(pref, short=switches['short'],
                                pad=switches['pad'])
        if switches['bland']:
            # Colorless output
            return pref_out
        return mark.pref.effects + pref_out + mark.text.effects

    def _prefix(self, pref: str, short: bool = None, pad: bool = None) -> str:
        '''
        prepend spaces and [ ] to make it pretty
        '''
        if short is None:
            short = self.switches['short']
        if pad is None:
            pad = self.switches['pad']
        preflen = len(pref)
        if not pref:
            preflen = - 2
        pad_len = 1 - preflen if short else self.max_info_size - preflen
        if pad_len < 0:
            pad_len = 0
        prefix = f"[{pref}]" if pref else ""
        padstr = " " + " " * pad_len
        return prefix + padstr * pad

    @staticmethod
    def _new_mark(base_pref: InfoMark = None, **kwargs) -> InfoMark:
        '''
        Generate a new mark
        '''
        pref_args = {}
        for key, default in DEFAULT_STYLE.items():
            if f'pref_{key}' in kwargs:
                pref_args[key] = kwargs[f'pref_{key}']
        text_args = {}
        for key, default in DEFAULT_STYLE.items():
            if f'text_{key}' in kwargs:
                text_args[key] = kwargs[f'text_{key}']
        pref_long_str = kwargs.get('pref_long_str', '')
        pref_short_str = kwargs.get('pref_short_str', '>')
        return InfoMark(parent=base_pref,
                        pref_long_str=pref_long_str,
                        pref_short_str=pref_short_str,
                        pref_args=pref_args, text_args=text_args)

    def _which_mark(self, pref: StrInt = None, **kwargs) -> InfoMark:
        '''
        Define a mark based on arguments supplied
        may be a pre-defined mark
        OR
        mark defined on the fly
        '''
        base_pref = None
        if pref is not None:
            # Pre-defined mark
            if isinstance(pref, int):
                if not 0 <= pref < len(self.info_index):
                    pref = 0
                base_pref = self.info_style[self.info_index[pref]]
            elif isinstance(pref, str):
                base_pref = self.info_style.get(pref, self.info_style['cont'])
            else:
                raise TypeError(f"{pref} should be either str or int")
        return self._new_mark(base_pref, **kwargs)

    def psprint(self, *args, pref: StrInt = None, **kwargs) -> None:
        '''
        *args: passed to print_function for printing
        pref: str/int: pre-declared InfoMark defaults: {
        cont: or 0 or anything else
        info: or 1
        act:  or 2
        list: or 3
        warn: or 4
        error:or 5
        bug:  or 6 } OR in **kwargs {
        pref_color: int/str (7)
        pref_gloss: int/str (1)
        pref_bgcol: int/str (0)
        text_color: int/str (7)
        text_gloss: int/str (1)
        text_bgcol: int/str (0)
        pref_long_str:  ""
        pref_short_str:  ">"
        }
        pad: if true, print with padding after pref
        short: if true, use {pref_short_str} instead
        bland: colorless
        disabled: behave like print_function
        file: passed to print function
        sep: passed to print function
        end: passed to print function
        flush: passed to print function
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

        args = list(args)
        mark = self._which_mark(pref=pref, **kwargs)
        args[0] = self._prefix_mark(mark=mark, **switches) + str(args[0])
        if not switches['bland']:
            args[-1] = str(args[-1]) + Style.RESET_ALL
        print(*args, **print_kwargs)

    def set_opts(self, rcfile) -> None:
        '''
        infile: rc file to read
        '''
        conf = ConfigParser()
        conf.read(rcfile)
        for mark in conf:
            if mark == "DEFAULT":
                for b_sw in self.switches:
                    self.switches[b_sw] =\
                        conf[mark].getboolean(b_sw, fallback=False)
                self.print_kwargs['sep'] =\
                    conf[mark].get("sep", fallback="\t")
                self.print_kwargs['end'] =\
                    conf[mark].get("end", fallback="\n")
                self.print_kwargs['flush'] =\
                    conf[mark].getboolean("flush", fallback=False)
                fname = conf[mark].get("file", fallback=None)  # Discouraged
                if fname is not None:
                    self.print_kwargs['file'] = open(fname, "a")
            else:
                try:
                    self.edit_style(index_str=mark, **conf[mark])
                except ValueError as err:
                    print()
                    print(f"'{mark}' from {rcfile}")
                    print("couldn't be parsed due to following error:")
                    print(f"'{err}'")
                    print()

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
                    and their light versions
        styles: 0:RESET_ALL\t1:NORMAL\t2:DIM\t3:BRIGHT

        returns the new (updated) info_style
        '''
        if index_handle is None or \
           not 0 <= index_handle <= len(self.info_index):
            self.info_index.append(index_str)
        else:
            self.info_index.insert(index_handle, index_str)
        self.info_style[index_str] = \
            self._new_mark(pref_long_str=pref_long_str, **kwargs)
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

