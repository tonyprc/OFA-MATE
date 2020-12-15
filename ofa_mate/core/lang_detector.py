#!/usr/bin/python3
# -*- coding: utf-8 -*-
# OFA Mate V.1.0.0 for OFA ParaConc
# Copyright (c) 2020 Tony Chang (42716403@qq.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys,os, re

class LangDetector:
    def __int__(self):
        pass

    # opt_organizer_group
    def detect_lang(self, text):
        target_lang = 'en'
        if text[0].isdigit():
            target_lang = 'num'
        else:
            for word in text:
                if '\u4e00' <= word <= '\u9fa5' or '\u3400' <= word <= '\u4DB5':
                    target_lang = 'zh'
                    break
        return target_lang

    # opt_organizer_group
    def detect_lang_swap(self, fc_dict, fc_lg, sent_list):

        def detect_lang(self, text):
            target_lang = 'en'
            if text[0].isdigit():
                target_lang = 'num'
            else:
                for word in text:
                    if '\u4e00' <= word <= '\u9fa5' or '\u3400' <= word <= '\u4DB5':
                        target_lang = 'zh'
                        break
            return target_lang

        num_lang_dict = {}
        for i, x in enumerate(sent_list[:10]):
            lang = self.detect_lang(x)
            num_lang_dict[str(i)] = lang
        if num_lang_dict['0'] == 'en' and num_lang_dict['1'] == 'zh':
            self.sl = 'en'
            self.tl = 'zh'
            lang_status = fc_dict['u_d'][fc_lg]
            sl_num_list = [i for i, y in num_lang_dict.items() if y == 'en']
            sl_check_list = list(
                map(lambda x: eval(sl_num_list[x]) - eval(sl_num_list[x - 1]), range(1, len(sl_num_list))))
            lang_gap = sl_check_list[0] - 1
        elif num_lang_dict['0'] == 'zh' and num_lang_dict['1'] == 'en':
            self.sl = 'zh'
            self.tl = 'en'
            lang_status = fc_dict['u_d'][fc_lg]
            sl_num_list = [i for i, y in num_lang_dict.items() if y == 'zh']
            sl_check_list = list(
                map(lambda x: eval(sl_num_list[x]) - eval(sl_num_list[x - 1]), range(1, len(sl_num_list))))
            lang_gap = sl_check_list[0] - 1
        elif num_lang_dict['0'] == 'num' and num_lang_dict['1'] == 'zh' and num_lang_dict['1'] == 'en':
            self.sl = 'zh'
            self.tl = 'en'
            lang_status = fc_dict["l_r"][fc_lg]
            lang_gap = 1
        elif num_lang_dict['0'] == 'num' and num_lang_dict['1'] == 'en' and num_lang_dict['1'] == 'zh':
            self.sl = 'en'
            self.tl = 'zh'
            lang_status = fc_dict["l_r"][fc_lg]
            lang_gap = 1
        else:
            self.sl = 'en'
            self.tl = 'zh'
            lang_status = fc_dict["bi-sep"][fc_lg]
            lang_gap = 0
        return lang_status, lang_gap, self.sl, self.tl