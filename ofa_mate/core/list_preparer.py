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

import os, json

from ofa_mate.ui.ui_main_window import UIMainWindow
from ofa_mate.core.info_collector import InfoCollector
from ofa_mate.core.lang_detector import LangDetector

class ListPreparer:
    '''Prepare bi_list for display and output'''
    def __init__(self):
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self._outPutDir = os.path.join(currentDir, "savedfiles")
        self._interface_lang_file = os.path.join(workFileDir, 'interface_language_setting.txt')
        self._interface_lang_dict = os.path.join(workFileDir, 'interface_language_dict.json')
        self.fc_lg, self.fc_dict = self.set_lang()
        ui = UIMainWindow()
        self._info_collector = InfoCollector()
        self._lang_detector = LangDetector()

    def set_lang(self):
        with open (self._interface_lang_file, mode = 'r', encoding = 'utf-8-sig') as f:
            default_lg = f.read().strip()
        with open (self._interface_lang_dict, mode = 'r', encoding = 'utf-8-sig') as f:
            lg_dict = json.loads(f.read())
        return default_lg, lg_dict

    # para_list_output_group
    # modify to a closed package
    def prepare_seperate_bi_list(self, ui, opt_dict, sc_lg, tg_lg, sl_para_list, tl_para_list):
        if opt_dict['marker_id'] == 1 and opt_dict['marker_chapt'] == 1:
            sl_num_list = [x.split('\t')[0] for x in sl_para_list]
            sl_sent_list = [x.split('\t')[1] for x in sl_para_list]
            sl_chapter_list = [x.split('\t')[2] for x in sl_para_list]
            tl_num_list = [x.split('\t')[0] for x in tl_para_list[0]]
            tl_sent_list = [x.split('\t')[1] for x in tl_para_list[0]]
            tl_chapter_list = [x.split('\t')[2] for x in tl_para_list[0]]
        elif opt_dict['marker_id'] == 1:
            sl_num_list = [x.split('\t')[0] for x in sl_para_list]
            sl_sent_list = [x.split('\t')[1] for x in sl_para_list]
            sl_chapter_list = []
            tl_num_list = [x.split('\t')[0] for x in tl_para_list[0]]
            tl_sent_list = [x.split('\t')[1] for x in tl_para_list[0]]
            tl_chapter_list = []
        elif opt_dict['marker_chapt'] == 1:
            sl_num_list = []
            sl_sent_list = [x.split('\t')[0] for x in sl_para_list]
            sl_chapter_list = [x.split('\t')[1] for x in sl_para_list]
            tl_num_list = []
            tl_sent_list = [x.split('\t')[0] for x in tl_para_list[0]]
            tl_chapter_list = [x.split('\t')[1] for x in tl_para_list[0]]
        else:
            sl_num_list = []
            sl_sent_list = [x.split('\t')[1] for x in sl_para_list]
            sl_chapter_list = []
            tl_num_list = []
            tl_sent_list = [x.split('\t')[1] for x in tl_para_list[0]]
            tl_chapter_list = []
        if sl_sent_list:
            sc_lg = self._lang_detector.detect_lang(sl_sent_list[0])
            if sc_lg == "en":
                tg_lg = "zh"
            else:
                sc_lg = "zh"
                tg_lg = "en"
            if sc_lg == "en":
                tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                
                try:
                    tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                except:
                    ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                    tmp_tl_title = ''
                    tmp_tl_author = ''
                    tmp_tl_translator = ''
                    tmp_tl_date = ''                    
            else:
                try:
                    tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                        sc_lg,tg_lg, sl_sent_list)
                except:
                    ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                    tmp_sl_title = ''
                    tmp_sl_author = ''
                    tmp_sl_translator = ''
                    tmp_sl_date = ''
                    
                tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                    sc_lg,tg_lg,tl_sent_list)

        else:
            tmp_sl_title = ''
            tmp_sl_author = ''
            tmp_sl_translator = ''
            tmp_sl_date = ''
            tmp_tl_title = ''
            tmp_tl_author = ''
            tmp_tl_translator = ''
            tmp_tl_date = ''
            
        if tmp_sl_title:
            ui._ss_book_titleBox.setText(tmp_sl_title)
            ui._ss_book_authorBox.setText(tmp_sl_author)
            ui._ss_book_translatorBox.setText(tmp_sl_translator)
            ui._ss_book_dateBox.setText(tmp_sl_date)
            ui._ss_book_languageBox.setText(sc_lg)
            ui._ss_book_genreBox.setText('')
            sl_text = "\n".join(sl_para_list)
            sl_text = sl_text.replace('ZZZZZ.', '')
            ui._ss_book_contentsBox.setText(sl_text)
            ui._tt_book_titleBox.setText(tmp_tl_title)
            ui._tt_book_authorBox.setText(tmp_tl_author)
            ui._tt_book_translatorBox.setText(tmp_tl_translator)
            ui._tt_book_dateBox.setText(tmp_tl_date)
            ui._tt_book_languageBox.setText(tg_lg)
            ui._tt_book_genreBox.setText('')
            tl_text = "\n".join(tl_para_list[0])
            ui._tt_book_contentsBox.setText(tl_text)
            ui._promptBox.setText(ui._prompt_2)
        else:
            ui._set_status_text(self.fc_dict["warning_read_fail_mark"][self.fc_lg])
        return sl_para_list, tl_para_list

    # para_list_output_group
    def prepare_return_bi_list(self, ui, sl_para_list, tl_para_list, temp_list, opt_dict, sc_lg, tg_lg, marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list):
        for num in range(row_max):
            sep_list = [item for item in para_list [num::row_max]]
            temp_list.append(sep_list)
        if marker_id_status == 1:
            if file_pos == self.fc_dict["u_d"][self.fc_lg]:
                for item in temp_list[0]:
                    sl_para_list.append(item.replace('ZZZZZ.', ''))
                for item in temp_list[1:]:
                    tl_para_list.append(item)
            else:
                sl_para_list = []
                tl_para_list = []
            if col_max == 2:
                sl_num_list = [x.split('\t')[0] for x in sl_para_list]
                sl_sent_list = [x.split('\t')[1] for x in sl_para_list]
                tl_num_list = [x.split('\t')[0] for x in tl_para_list[0]]
                tl_sent_list = [x.split('\t')[1] for x in tl_para_list[0]]
                if sc_lg == "en":
                    tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    try:
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_tl_title = ''
                        tmp_tl_author = ''
                        tmp_tl_translator = ''
                        tmp_tl_date = ''
                else:
                    try:
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                            sc_lg,tg_lg,sl_sent_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_sl_title = ''
                        tmp_sl_author = ''
                        tmp_sl_translator = ''
                        tmp_sl_date = ''

                    tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                        sc_lg,tg_lg,tl_sent_list)
                    
            elif col_max == 3:
                sl_num_list = [x.split('\t')[0] for x in sl_para_list]
                sl_sent_list = [x.split('\t')[1] for x in sl_para_list]
                sl_chapter_list = [x.split('\t')[2] for x in sl_para_list]
                tl_num_list = [x.split('\t')[0] for x in tl_para_list[0]]
                tl_sent_list = [x.split('\t')[1] for x in tl_para_list[0]]
                tl_chapter_list = [x.split('\t')[2] for x in tl_para_list[0]]
                
                if sc_lg == "en":
                    tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    try:
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                    except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_tl_title = ''
                            tmp_tl_author = ''
                            tmp_tl_translator = ''
                            tmp_tl_date = ''
                else:
                    try:
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                            sc_lg,tg_lg,sl_sent_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_sl_title = ''
                        tmp_sl_author = ''
                        tmp_sl_translator = ''
                        tmp_sl_date = ''

                    tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                        sc_lg,tg_lg,tl_sent_list)
            else:
                tmp_sl_title = ''
                tmp_sl_author = ''
                tmp_sl_translator = ''
                tmp_sl_date = ''
                tmp_tl_title = ''
                tmp_tl_author = ''
                tmp_tl_translator = ''
                tmp_tl_date = ''
            if tmp_sl_title:
                ui._ss_book_titleBox.setText(tmp_sl_title)
                ui._ss_book_authorBox.setText(tmp_sl_author)
                ui._ss_book_translatorBox.setText(tmp_sl_translator)
                ui._ss_book_languageBox.setText(sc_lg)
                ui._ss_book_dateBox.setText(tmp_sl_date)
                ui._ss_book_genreBox.setText('')
                sl_text = "\n".join(sl_para_list)
                sl_text = sl_text.replace('ZZZZZ.', '')
                ui._ss_book_contentsBox.setText(sl_text)
                ui._tt_book_titleBox.setText(tmp_tl_title)
                ui._tt_book_authorBox.setText(tmp_tl_author)
                ui._tt_book_translatorBox.setText(tmp_tl_translator)
                ui._tt_book_languageBox.setText(tg_lg)
                ui._tt_book_dateBox.setText(tmp_tl_date)
                ui._tt_book_genreBox.setText('')
                tl_text = "\n".join(tl_para_list[0])
                ui._tt_book_contentsBox.setText(tl_text)
                ui._promptBox.setText(ui._prompt_2)
            else:
                ui._set_status_text(self.fc_dict["warning_read_fail_mark"][self.fc_lg])
        else:
            if file_pos == self.fc_dict["u_d"][self.fc_lg]:
                for item in temp_list[0]:
                    sl_para_list.append(item.replace('ZZZZZ.', ''))
                for item in temp_list[1:]:
                    tl_para_list.append(item)
            else:
                 sl_para_list = []
                 tl_para_list = []
            if col_max == 1:
                sl_list = sl_para_list
                tl_list = tl_para_list[0]
                if sc_lg == 'en':
                    tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_en(
                        sc_lg,tg_lg,sl_list)
                    try:
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(
                            sc_lg,tg_lg,tl_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_tl_title = ''
                        tmp_tl_author = ''
                        tmp_tl_translator = ''
                        tmp_tl_date = ''                        
                else:
                    try:
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                            sc_lg,tg_lg,sl_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_sl_title = ''
                        tmp_sl_author = ''
                        tmp_sl_translator = ''
                        tmp_sl_date = ''
                        
                    tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                        sc_lg,tg_lg,tl_list)
                    
            elif col_max == 2:
                sl_list = sl_para_list
                tl_list = tl_para_list[0]
                sl_sent_list = [x.split('\t')[0] for x in sl_list]
                sl_chapter_list = [x.split('\t')[1] for x in sl_list]
                tl_sent_list = [x.split('\t')[0] for x in tl_list]
                tl_chapter_list = [x.split('\t')[1] for x in tl_list]
                if sc_lg == 'en':
                    tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    try:
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_tl_title = ''
                        tmp_tl_author = ''
                        tmp_tl_translator = ''
                        tmp_tl_date = ''                        
                else:
                    try:
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                            sc_lg,tg_lg,sl_sent_list)
                    except:
                        ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                        tmp_sl_title = ''
                        tmp_sl_author = ''
                        tmp_sl_translator = ''
                        tmp_sl_date = ''
                        
                    tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                        sc_lg,tg_lg,tl_sent_list)
            else:
                tmp_sl_title = ''
                tmp_sl_author = ''
                tmp_sl_translator = ''
                tmp_sl_date = ''
                tmp_tl_title = ''
                tmp_tl_author = ''
                tmp_tl_translator = ''
                tmp_tl_date = ''
            if tmp_sl_title:                
                ui._ss_book_titleBox.setText(tmp_sl_title)
                ui._ss_book_authorBox.setText(tmp_sl_author)
                ui._ss_book_translatorBox.setText(tmp_sl_translator)
                ui._ss_book_languageBox.setText(sc_lg)
                ui._ss_book_dateBox.setText(tmp_sl_date)
                ui._ss_book_genreBox.setText('')
                ui._ss_book_contentsBox.setText(
                    "\n".join([x[:50] + "..." if len(x) > 50 else x for x in sl_para_list]))                     
                ui._tt_book_titleBox.setText(tmp_tl_title)
                ui._tt_book_authorBox.setText(tmp_tl_author)
                ui._tt_book_translatorBox.setText(tmp_tl_translator)
                ui._tt_book_languageBox.setText(tg_lg)
                ui._tt_book_dateBox.setText(tmp_tl_date)
                ui._tt_book_genreBox.setText('')
                ui._tt_book_contentsBox.setText(
                    "\n".join([y[:25] + "..." if len(y) > 25 else y for y in tl_para_list[0]]))
                ui._promptBox.setText(ui._prompt_2)
            else:
                ui._set_status_text(self.fc_dict["warning_read_fail_mark"][self.fc_lg])

        return sl_para_list, tl_para_list

    # para_list_output_group
    def prepare_tab_bi_list(self, ui, sl_para_list, tl_para_list,temp_list,opt_dict, sc_lg, tg_lg, marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list):
        # 路径：有行号(无标题|有标题)|无行号(无标题|有标题)
        # 按总列数组织临时列表[[列0],[列1]...]
        for num in range(col_max):
            sep_list = [item.split('\t')[num].replace("ZZZZZ.", "") for item in para_list]
            temp_list.append(sep_list)
        # 如果有行号，列0为行号
        if opt_dict['marker_id'] == 1:
            # 总列数为3或4时，不可能含篇章标题，列1,列2，列3为英、汉，汉，生成[序号,语1]两列英文段落列表与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
            if 3 <= col_max <= 4:
                if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                    sl_para_list.extend(x + '\t' + y for (x, y) in list(zip(temp_list[0], temp_list[1])))  # zip一定要转成列表，否则深层数据提出不出来
                    i = 2
                    while i < col_max:
                        tl_list = []
                        for (x, y) in zip(temp_list[0], temp_list[i]):
                            tl_str = x + '\t' + y
                            tl_list.append(tl_str)
                        tl_para_list.append(tl_list)
                        i += 1
            # 总列数大于等于5时，可能含标题
            elif col_max >= 5:
                # 有篇章标题时，列1,英，列2，标题，列3，中1，列4，标题....
                if marker_chapter == 1:
                    if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                        sl_para_list.extend(x + '\t' + y + '\t'+ z for (x, y, z) in list(zip(temp_list[0], temp_list[1], temp_list[2])))
                        i = 3
                        while i < col_max:
                            j = i + 1
                            tl_list = []
                            for (x, y, z) in zip(temp_list[0], temp_list[i], temp_list[j]):
                                tl_str = x + '\t' + y + '\t' + z
                                tl_list.append(tl_str)
                            tl_para_list.append(tl_list)
                            i = j
                            i += 1
                else:
                    # 无篇章标题时，列1,列2，列3...为英，汉，汉...生成[序号,语1]两列英文段落列表
                    # 与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
                    if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                        sl_para_list.extend(x + '\t' + y  for (x, y) in list(zip(temp_list[0], temp_list[1])))  # zip一定要转成列表，否则深层数据提出不出来
                        i = 2
                        while i < col_max:
                            tl_list = []
                            for (x, y) in zip(temp_list[0], temp_list[i]):
                                a_str = x + '\t' + y
                                tl_list.append(a_str)
                            tl_para_list.append(tl_list)
                            i += 1
            else:
                sl_para_list.clear()
                tl_para_list.clear()
            if sl_para_list == []:
                ui._set_status_text(self.fc_dict["warning_read_fail_col"][self.fc_lg])
                tmp_sl_title = ''
                tmp_sl_author = ''
                tmp_sl_translator = ''
                tmp_sl_date = ''
                tmp_tl_title = ''
                tmp_tl_author = ''
                tmp_tl_translator = ''
                tmp_tl_date = ''
            else:
                if marker_chapter == 0:
                    sl_num_list = [item.split('\t')[0] for item in sl_para_list]
                    sl_sent_list = [item.split('\t')[1] for item in sl_para_list]
                    if sc_lg == 'en':
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    else:
                        try:
                            tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                                sc_lg,tg_lg,sl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_sl_title = ''
                            tmp_sl_author = ''
                            tmp_sl_translator = ''
                            tmp_sl_date = ''
                    tl_num_list = [item.split('\t')[0] for item in tl_para_list[0]]
                    tl_sent_list = [item.split('\t')[1] for item in tl_para_list[0]]
                    if tg_lg == 'en':
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,tl_sent_list)
                    else:
                        try:
                            tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(
                                sc_lg,tg_lg,tl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_tl_title = ''
                            tmp_tl_author = ''
                            tmp_tl_translator = ''
                            tmp_tl_date = ''
                else:
                    sl_num_list = [item.split('\t')[0] for item in sl_para_list]
                    sl_sent_list = [item.split('\t')[1] for item in sl_para_list]
                    sl_chapter_list = [item.split('\t')[2] for item in sl_para_list]
                    if sc_lg == 'en':
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    else:
                        try:
                            tmp_sl_title, tmp_sl_author, tmp_sl_translator, tmp_sl_date = self._info_collector.info_collector_zh(
                                sc_lg,tg_lg,sl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_sl_title = ''
                            tmp_sl_author = ''
                            tmp_sl_translator = ''
                            tmp_sl_date = ''
                    tl_num_list = [item.split('\t')[0] for item in tl_para_list[0]]
                    tl_sent_list = [item.split('\t')[1] for item in tl_para_list[0]]
                    tl_chapter_list = [item.split('\t')[2] for item in tl_para_list[0]]
                    if tg_lg == 'en':
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(
                            sc_lg,tg_lg,tl_sent_list)
                    else:
                        try:
                            tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg, tl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_tl_title = ''
                            tmp_tl_author = ''
                            tmp_tl_translator = ''
                            tmp_tl_date = ''
            if tmp_sl_title:
                ui._ss_book_titleBox.setText(tmp_sl_title)
                ui._ss_book_authorBox.setText(tmp_sl_author)
                ui._ss_book_languageBox.setText(sc_lg)
                ui._ss_book_dateBox.setText(tmp_sl_date)
                ui._ss_book_genreBox.setText('')
                sl_text = "\n".join(sl_para_list)
                sl_text = sl_text.replace('ZZZZZ.', '')
                ui._ss_book_contentsBox.setText(sl_text)
                ui._tt_book_titleBox.setText(tmp_tl_title)
                ui._tt_book_languageBox.setText(tg_lg)
                ui._tt_book_authorBox.setText(tmp_tl_author)
                ui._tt_book_translatorBox.setText(tmp_tl_translator)
                ui._tt_book_dateBox.setText(tmp_tl_date)
                ui._tt_book_genreBox.setText('')
                tl_text = "\n".join(tl_para_list[0])
                ui._tt_book_contentsBox.setText(tl_text)
                ui._promptBox.setText(ui._prompt_2)
            else:
                ui._set_status_text(self.fc_dict["warning_read_fail_mark"][self.fc_lg])
        else:
            # 无篇章标题：列0英，列1中，列2中...
            # 有篇章标题：列0英，列1英标题，列2中,列3中标题，列4中，列5中标题
            # 总列数为2或3时，不可能含篇章标题，列0,列1，列2为英、汉，汉，生成[序号,语1]两列英文段落列表与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
            if 2 <= col_max <= 3:
                if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                    sl_para_list.extend(temp_list[0])
                    i = 1
                    while i < col_max:
                        tl_para_list.append(temp_list[i])
                        i += 1

            # 总列数大于等于4时，可能含标题
            elif col_max >= 4:
                # 有篇章标题时，列0,英，列1，英标题，列2，中，列3，中标题....
                if marker_chapter == 1:
                    if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                        sl_para_list.extend(x + '\t' + y for (x, y) in list(zip(temp_list[0], temp_list[1])))
                        i = 2
                        while i < col_max:
                            j = i + 1
                            tl_list = []
                            for (x, y) in zip(temp_list[0], temp_list[i]):
                                a_str = x + '\t' + y
                                tl_list.append(a_str)
                            tl_para_list.append(tl_list)
                            i = j
                            i += 1
                else:
                    # 无篇章标题时，列0,英,列1,汉,列2，汉
                    if file_pos == self.fc_dict["l_r"][self.fc_lg]:
                        sl_para_list.extend(temp_list[0])  # zip一定要转成列表，否则深层数据提出不出来
                        i = 1
                        while i < col_max:
                            tl_para_list.append(temp_list[i])
                            i += 1
            else:
                sl_para_list.clear()
                tl_para_list.clear()
            if sl_para_list == []:
                ui._set_status_text(self.fc_dict["warning_read_fail_col"][self.fc_lg])
                tmp_sl_title = ''
                tmp_sl_author = ''
                tmp_sl_translator = ''
                tmp_sl_date = ''
                tmp_tl_title = ''
                tmp_tl_author = ''
                tmp_tl_translator = ''
                tmp_tl_date = ''
            else:
                if marker_chapter == 1:
                    sl_sent_list = [item.split('\t')[0] for item in sl_para_list]
                    sl_chapter_list = [item.split('\t')[1] for item in sl_para_list]
                    if sc_lg == 'en':
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    else:
                        try:
                            tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,sl_sent_list)
                        except:
                            tmp_sl_title = ''
                            tmp_sl_author = ''
                            tmp_sl_translator = ''
                            tmp_sl_date = ''
                    tl_sent_list = [item.split('\t')[0] for item  in tl_para_list[0]]
                    tl_chapter_list = [item.split('\t')[1] for item  in tl_para_list[0]]
                    if tg_lg == 'en':
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,tl_sent_list)
                    else:
                        try:
                            tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_tl_title = ''
                            tmp_tl_author = ''
                            tmp_tl_translator = ''
                            tmp_tl_date = ''
                else:
                    sl_sent_list = sl_para_list
                    if sc_lg == 'en':
                        tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,sl_sent_list)
                    else:
                        try:
                            tmp_sl_title, tmp_sl_author, tmp_sl_translator,tmp_sl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,sl_sent_list)
                        except:
                            tmp_sl_title = ''
                            tmp_sl_author = ''
                            tmp_sl_translator = ''
                            tmp_sl_date = ''
                    tl_sent_list = tl_para_list[0]
                    if tg_lg == 'en':
                        tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_en(sc_lg,tg_lg,tl_sent_list)
                    else:
                        try:
                            tmp_tl_title, tmp_tl_author, tmp_tl_translator, tmp_tl_date = self._info_collector.info_collector_zh(sc_lg,tg_lg,tl_sent_list)
                        except:
                            ui._set_status_text(self.fc_dict["warning_zh_fail"][self.fc_lg])
                            tmp_tl_title = ''
                            tmp_tl_author = ''
                            tmp_tl_translator = ''
                            tmp_tl_date = ''
            if tmp_sl_title:
                ui._ss_book_titleBox.setText(tmp_sl_title)
                ui._ss_book_authorBox.setText(tmp_sl_author)
                ui._ss_book_dateBox.setText(tmp_sl_date)
                ui._ss_book_languageBox.setText(sc_lg)
                ui._ss_book_genreBox.setText('')
                sl_text = "\n".join(sl_para_list)
                sl_text = sl_text.replace('ZZZZZ.', '')
                ui._ss_book_contentsBox.setText(sl_text)
                ui._tt_book_titleBox.setText(tmp_tl_title)
                ui._tt_book_authorBox.setText(tmp_tl_author)
                ui._tt_book_languageBox.setText(tg_lg)
                ui._tt_book_translatorBox.setText(tmp_tl_translator)
                ui._tt_book_dateBox.setText(tmp_tl_date)
                ui._tt_book_genreBox.setText('')
                tl_text = "\n".join(tl_para_list[0])
                ui._tt_book_contentsBox.setText(tl_text)
                ui._promptBox.setText(ui._prompt_2)
            else:
                ui._set_status_text(self.fc_dict["warning_read_fail_mark"][self.fc_lg])
        return sl_para_list, tl_para_list