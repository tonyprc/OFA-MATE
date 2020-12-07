#!/usr/bin/python3
# -*- coding: utf-8 -*-
# OFA Mate V.1.0.0 for OFA ParaConc
# Copyright (c) 2020 Tony96163 (42716403@qq.com)

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

import os, re,json, xlrd
from docx import Document
from collections import defaultdict
from PyQt5.QtWidgets import QFileDialog

from ofa_mate.ui.ui_main_window import UIMainWindow
from ofa_mate.core.info_collector import InfoCollector
from ofa_mate.core.chapter_filler import ChapterFiller

class MainWindow:
    def __init__(self):
        currentDir = os.getcwd()
        self._outPutDir = os.path.join(currentDir, "savedfiles")

        # recieve signals
        self._ui = UIMainWindow()
        self._ui.open_file.connect(self.open_file)
        self._ui.reload_file.connect(self.reload_file)        
        self._ui.load_next_version.connect(self.load_next_version)
        self._ui.write_to_json.connect(self.write_to_json)
        self._ui.json_en_filler.connect(self.json_en_filler)
        self._ui.json_zh_filler.connect(self.json_zh_filler)
        self._ui.json_en_refiller.connect(self.json_en_refiller)
        self._ui.json_zh_refiller.connect(self.json_zh_refiller)

        self._info_collector = InfoCollector()
        self._chapter_maker = ChapterFiller()
     
        # data preparation
        self._opt_dict = {}
        self._temp_list = []
        self._file_suffix = ""

        self._current_file = ''
        self._current_file_list = []
        self._file_id_list = []
        
        self._current_en_para_list = []
        self._current_zh_para_list = []
        self._current_en_chapter_num_list = []

        self._en_bookDict = {}
        self._zh_bookDict_list = []

        self._current_dict_key = ""
        self._current_en_dict_version = ""
        self._current_zh_dict_version = "" 

        self._ui.show()

    def open_single_file(self, target_file):
        para_list = []
        if self._ui._file_openBox.text():
            self.form_reset()
            if target_file.endswith('txt'):
                with open(target_file, 'rt', encoding = 'utf-8-sig') as f:
                    text = f.read()
                    if "<seg" in text:
                        self._ui._file_cuc_mark_box.setChecked(True)
                        self._opt_dict['marker_seg'] = 1
                        text = re.sub(r'<seg.*"(\d+)"?>(.*)?</seg>', '\g<1>\t\g<2>', text)
                    else:
                        pass
                    para_list = text.split('\n')
                if para_list:
                    self.file_evaluator(para_list)
                else:
                    pass
            elif target_file.endswith('docx'):
                file_pos = self._opt_dict['lang_pos']
                form_marker = self._opt_dict['marker_table']
                self._ui._file_cuc_mark_box.setChecked(False)
                self._opt_dict['marker_seg'] = 0
                self._ui._file_chapt_num_box.setChecked(False)
                self._opt_dict['marker_chapt'] = 0
                self._ui._file_portion_box.setValue(1)
                self._opt_dict['lang_cols'] = 1

                # 无表格标记
                if form_marker == 0:
                    self._ui._file_pos_box.setCurrentIndex(0)
                    self._opt_dict['lang_pos'] = '英上中下'
                    self._ui._file_tab_mark_box.setChecked(False)
                    self._opt_dict['marker_tab'] = 0
                    with open(target_file, 'rb') as doc:
                        document = Document(doc)
                        para_list = [para.text.strip() for para in document.paragraphs]
                    # 列表为空字串，转为靠长度判断其是否为有效列表
                    list_length = len(para_list)
                    if list_length > 1:
                        pass
                    else:
                        # 列表为空字串，自动补填表格标记并更新字典值，直接尝试读取表格
                        para_list = []
                        with open(target_file, 'rb') as doc:
                            document = Document(doc)
                            tables = document.tables
                            for table in tables[:]:
                                for i, row in enumerate(table.rows[:]):
                                    row_content = []
                                    for cell in row.cells[:]:
                                        c = cell.text
                                        row_content.append(c)
                                    row_string = '\t'.join(row_content)
                                    para_list.append(row_string)
                        list_length = len(para_list)
                        if list_length > 1:
                            self._ui._file_table_mark_box.setChecked(True)
                            self._opt_dict['marker_table'] = 1
                            self._ui._file_pos_box.setCurrentIndex(2)
                            self._opt_dict['lang_pos'] = '英左中右'
                            self._ui._file_tab_mark_box.setChecked(False)
                            self._opt_dict['marker_tab'] = 0
                        else:
                            para_list = []
                # 有表格标记
                else:
                    self._ui._file_pos_box.setCurrentIndex(2)
                    self._opt_dict['lang_pos'] = '英左中右'
                    self._ui._file_tab_mark_box.setChecked(False)
                    self._opt_dict['marker_tab'] = 0
                    para_list = []
                    with open(target_file, 'rb') as doc:
                        document = Document(doc)
                        tables = document.tables
                        for table in tables[:]:
                            for i, row in enumerate(table.rows[:]):
                                row_content = []
                                for cell in row.cells[:]:
                                    c = cell.text
                                    row_content.append(c)
                                row_string = '\t'.join(row_content)
                                para_list.append(row_string)
                    list_length = len(para_list)
                    if list_length > 1:
                        pass
                    else:
                        with open(target_file, 'rb') as doc:
                            document = Document(doc)
                            para_list = [para.text.strip() for para in document.paragraphs]
                        list_length = len(para_list)
                        if list_length > 1:
                            self._ui._file_pos_box.setCurrentIndex(0)
                            self._opt_dict['lang_pos'] = '英上中下'
                            self._ui._file_tab_mark_box.setChecked(False)
                            self._opt_dict['marker_tab'] = 0
                            self._ui._file_table_mark_box.setChecked(False)
                            self._opt_dict['marker_table'] = 0
                        else:
                            para_list = []
                if para_list:
                    self.file_evaluator(para_list)
                else:
                    self._ui._set_status_text("文件读取失败，请重试")
            elif target_file.endswith('xlsx'):
                self._ui._file_pos_box.setCurrentIndex(2)
                self._opt_dict['lang_pos'] = '英左中右'
                self._ui._file_table_mark_box.setChecked(True)
                self._opt_dict['marker_table'] = 1
                loc = (target_file)
                wb = xlrd.open_workbook(loc)
                sheet_id = wb.sheet_names()
                temp_para_list = []
                for v, text_id in enumerate(sheet_id):
                    sheet = wb.sheet_by_name(text_id)
                    content = []
                    for i in range(sheet.nrows):
                        content_line = []
                        for j in range(sheet.ncols):
                            line_content = sheet.cell_value(i, j)
                            # 防止序号为浮点数时显示小数点位
                            if isinstance(line_content, float):
                                line_content = str(int(line_content))
                            else:
                                pass
                            content_line.append(line_content)
                        content.append("\t".join(content_line))
                    temp_para_list.append(content)
                if temp_para_list:
                    for para_list in temp_para_list:
                        self.file_evaluator(para_list)
                elif self._current_en_para_list:
                    para_list = self._current_en_para_list
                    self.file_evaluator(para_list)
                else:
                    self._ui._set_status_text("文件读取失败，请重试")
            else:
                pass
        else:
            pass

    # file_open_group
    def open_multi_file(self, target_files, file_id_list):
        if self._ui._file_openBox.text():
            self.form_reset()
            if target_files:
                file_groups = []
                for filename in set(file_id_list):
                    s_list = []
                    for filepath in target_files:
                        if filename in filepath:
                            s_list.append(filepath)
                        else:
                            pass
                    file_groups.append(s_list)
                group_num = len(file_groups)
                for file_group in file_groups:
                    file_num = len(file_group)
                    self._ui._file_num_box.setValue(file_num)
                    self.form_reset()
                    en_para_list = []
                    zh_para_list = []
                    for file in file_group:
                        if 's0' in file:
                            with open(file, 'rt', encoding = 'utf-8-sig') as f:
                                text = f.read()
                                if "<seg" in text:
                                    self._ui._file_cuc_mark_box.setChecked(True)
                                    self._opt_dict['marker_seg'] = 1
                                    text = re.sub(r'<seg.*"(\d+)"?>(.*)?</seg>', '\g<1>\t\g<2>', text)
                                else:
                                    pass
                            para_list = text.split('\n')
                            en_para_list.extend([sent.strip().replace('ZZZZZ.', "") for sent in para_list])
                        elif 'EN' in file:
                            with open(file, 'rt', encoding = 'utf-8-sig') as f:
                                text = f.read()
                                if "<seg" in text:
                                    self._ui._file_cuc_mark_box.setChecked(True)
                                    self._opt_dict['marker_seg'] = 1
                                    text = re.sub(r'<seg.*"(\d+)"?>(.*)?</seg>', '\g<1>\t\g<2>', text)
                                else:
                                    pass
                            para_list = text.split('\n')
                            en_para_list.extend([sent.strip().replace('ZZZZZ.', "") for sent in para_list])
                        else:
                            with open(file, 'rt', encoding = 'utf-8-sig') as f:
                                text = f.read()
                                if "<seg" in text:
                                    self._ui._file_cuc_mark_box.setChecked(True)
                                    self._opt_dict['marker_seg'] = 1
                                    text = re.sub(r'<seg.*"(\d+)"?>(.*)?</seg>', '\g<1>\t\g<2>', text)
                                else:
                                    pass
                            para_list = text.split('\n')
                            zh_para_list.append([sent.strip() for sent in para_list])
                    self._current_en_para_list = en_para_list
                    self._current_zh_para_list = zh_para_list
                    if en_para_list:
                        self.file_evaluator(en_para_list)
                        self.prepare_seperate_bi_list(en_para_list, zh_para_list)
                    else:
                        self._current_file_list.clear()
                        self._ui._set_status_text('双语对齐txt多文件命名不统一，请正确命名相关文件')
            else:
                pass
        else:
            pass

    # file_open_group
    def reload_file(self):
        if self._ui._file_openBox.text():
            current_en_text = self._ui._ss_book_contentsBox.toPlainText()
            if current_en_text:
                self._ui._set_status_text("文件已成功加载，请勿反复加载!")
            else:
                self._opt_dict = self.opt_checker()
                file_type = self._opt_dict['file_type']
                if self._ui._file_openButton.text() == "打开单文件":
                    if self._current_file:
                        self.open_single_file(self._current_file)
                elif self._ui._file_openButton.text() == "打开多文件":
                    if self._current_file_list and self._file_id_list:
                        self.open_multi_file(self._current_file_list, self._file_id_list)
                    else:
                        self._current_file_list.clear()
                        self._file_id_list.clear()
                        self._ui._set_status_text('指定文件夹内未找到多语对齐txt文件，请正确命名相关文件')
                else:
                    pass
        else:
            self._ui._set_status_text('当前尚未加载任何文件，请先加载文件')

    # 打开单文件，只读取目标文件夹名称及路径，同时生成操作选项核对列表
    # file_open_group
    def open_file(self):
        self._opt_dict.clear()
        self._opt_dict = self.opt_checker()
        self._file_suffix = self._opt_dict['file_type']
        self.form_reset()
        file_type = self._opt_dict['file_type']
        if self._ui._file_openButton.text() == "打开单文件":
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            presentFile = QFileDialog.getOpenFileName(self._ui, "打开单文件", "", f"*.{self._file_suffix}", options = options)
            if presentFile:
                present_file_path = presentFile[0]
                present_file = present_file_path.split('/')[-1]
                self._ui._file_openBox.setText(present_file)
                self._current_file = present_file_path
                self.open_single_file(self._current_file)
        elif self._ui._file_openButton.text() == "打开多文件":
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            presentDir = QFileDialog.getExistingDirectory(self._ui, "打开多文件", "", options = options)
            if presentDir:
                working_dir = os.getcwd()
                self._current_file_list.clear()
                self._file_id_list.clear()
                file_list = os.listdir(presentDir)
                file_final_list = []
                for file in file_list:
                    if file.endswith('.txt'):
                        file_version = re.search(r's0|t\d+|EN|ZH', file)
                        file_id = re.sub(r's0|t\d+|EN|ZH', "", file)
                        file_id = re.sub(r'\.txt', "", file_id)
                        if file_version:
                            file_final_list.append(file)
                            self._file_id_list.append(file_id)
                            file_path = os.path.join(presentDir, file)
                            file_path = file_path.replace('\\', "/")
                            self._current_file_list.append(file_path)
                        else:
                            pass
                    else:
                        pass
                if file_final_list:
                    self._ui._file_openBox.setText(",".join(file_final_list))
                    self.open_multi_file(self._current_file_list, self._file_id_list)
                else:
                    pass
            else:
                self._current_file_list.clear()
                self._file_id_list.clear()
                self._ui._set_status_text('指定文件夹内未找到多语对齐txt文件，请正确命名相关文件')
        else:
            pass

    # opt_organizer_group
    def detect_lang(self, text):
        if text[0].isdigit() == True:
            target_lang = 'num'
        else:
            target_lang = 'en'
            for word in text:
                if '\u4e00' <= word <= '\u9fa5' or '\u3400' <= word <= '\u4DB5':
                    target_lang = 'zh'
                break
        return target_lang
    # opt_organizer_group
    def detect_lang_swap(self, sent_list):
        num_lang_dict = {}
        for i, x in enumerate(sent_list[:10]):
            lang = self.detect_lang(x)
            num_lang_dict[str(i)] = lang
        if num_lang_dict['0'] == 'en' and num_lang_dict['1'] == 'zh':
            lang_status = "英上中下"
            en_num_list = [i for i, y in num_lang_dict.items() if y == 'en']
            en_check_list = list(
                map(lambda x: eval(en_num_list[x]) - eval(en_num_list[x - 1]), range(1, len(en_num_list))))
            lang_gap = en_check_list[0] - 1
        elif num_lang_dict['0'] == 'zh' and num_lang_dict['1'] == 'en':
            lang_status = "中上英下"
            zh_num_list = [i for i, y in num_lang_dict.items() if y == 'zh']
            zh_check_list = list(
                map(lambda x: eval(zh_num_list[x]) - eval(zh_num_list[x - 1]), range(1, len(zh_num_list))))
            lang_gap = zh_check_list[0] - 1
        else:
            lang_status = "双语分离"
            lang_gap = 0
        return lang_status, lang_gap

    # opt_organizer_group
    def file_evaluator(self, para_list):
        lang_status_dict = {'英上中下': 0, '中上英下': 1, '英左中右': 2, '中左英右': 3, '双语分离': 4}
        if para_list == []:
            self._ui._set_status_text('文件读取出错，请检查选项是否选择有误！')
        else:
            tab_test = para_list[0].split('\t')
            if len(tab_test) == 1:
                col_max = 1
                marker_id_status = 0
                self._ui._file_num_mark_box.setChecked(False)
                self._opt_dict['marker_id'] = 0
                marker_chapter = 0
                self._ui._file_chapt_num_box.setChecked(False)
                self._opt_dict['marker_chapt'] = 0
                self._ui._file_tab_mark_box.setChecked(False)
                self._opt_dict['marker_tab'] = 0
                lang_status, lang_gap = self.detect_lang_swap(para_list)
                self._ui._file_portion_box.setValue(lang_gap)
                self._opt_dict['lang_cols'] = lang_gap
                if lang_status in ['英上中下', '中上英下', '英左中右', '中左英右', '双语分离']:
                    pos_index = lang_status_dict[lang_status]
                    self._ui._file_pos_box.setCurrentIndex(pos_index)
                    self._opt_dict['lang_pos'] = lang_status
                    if lang_status in ['英上中下', '中上英下']:
                        self._opt_dict['lang_rows'] = int(self._ui._file_portion_box.value()) + 1
                        self._opt_dict['lang_cols'] = 1
                    elif lang_status in ['英左中右', '中左英右']:
                        self._opt_dict['lang_rows'] = 1
                        self._opt_dict['lang_cols'] = int(self._ui._file_portion_box.value())
                    elif lang_status == '双语分离':
                        self._opt_dict['lang_rows'] = 1
                        self._opt_dict['lang_cols'] = 0
                    else:
                        pos_index = lang_status_dict[lang_status]
                        self._ui._file_pos_box.setCurrentIndex(pos_index)
                else:
                    pass
            elif len(tab_test) >= 2:
                col_max = len(tab_test)
                self._ui._file_tab_mark_box.setChecked(True)
                self._opt_dict['marker_tab'] = 1
                tab_list = []
                if '' not in tab_test:
                    for item in para_list:
                        item_list = item.split('\t')
                        tab_list.append(item_list)
                else:
                    for item in para_list:
                        item_list = item.split('\t')
                        if '' in item_list:
                            pass
                        else:
                            tab_list.append(item_list)
                colum_max = len(tab_list[0])
                lang_seq_dict = {}
                lang_seq_list = []
                for i in range(colum_max):
                    target_lang = self.detect_lang(tab_list[0][i])
                    lang_seq_dict[target_lang] = i
                    lang_seq_list.append(target_lang)
                count_col_num = lang_seq_list.count('num')
                count_col_en = lang_seq_list.count('en')
                count_col_zh = lang_seq_list.count('zh')
                col_names = [x for x in lang_seq_dict.keys()]
                col_name_string = ":".join(col_names)
                if 'en' in lang_seq_dict.keys() and "zh" in lang_seq_dict.keys():
                    if lang_seq_dict['en'] < lang_seq_dict['zh']:
                        lang_status = "英左中右"
                        if count_col_en == 1:
                            lang_gap = count_col_zh
                            self._ui._file_portion_box.setValue(lang_gap)
                            self._opt_dict['lang_cols'] = lang_gap
                            self._opt_dict['lang_rows'] = 1
                            title = "无标题"
                        else:
                            lang_gap = int(count_col_zh / 2)
                            self._ui._file_portion_box.setValue(lang_gap)
                            self._opt_dict['lang_cols'] = lang_gap
                            self._opt_dict['lang_rows'] = 1
                            title = '有标题'
                    else:
                        lang_status = "中左英右"
                        if count_col_zh == 1:
                            lang_gap = count_col_en
                            self._ui._file_portion_box.setValue(lang_gap)
                            self._opt_dict['lang_cols'] = lang_gap
                            self._opt_dict['lang_rows'] = 1
                            title = "无标题"
                        else:
                            lang_gap = int(count_col_en / 2)
                            self._ui._file_portion_box.setValue(lang_gap)
                            self._opt_dict['lang_cols'] = lang_gap
                            self._opt_dict['lang_rows'] = 1
                            title = '有标题'

                # 否则为上下结构
                elif 'en' in lang_seq_dict.keys():
                    if count_col_en == 1:
                        title = "无标题"
                    else:
                        title = '有标题'
                    col_sent_list = []
                    col_id = lang_seq_dict['en']
                    for item in tab_list:
                        col_sent_list.append(item[col_id])
                    lang_status, lang_gap = self.detect_lang_swap(col_sent_list)
                    self._ui._file_portion_box.setValue(lang_gap)
                    self._opt_dict['lang_cols'] = lang_gap
                    if lang_status == '双语分离':
                        self._opt_dict['lang_rows'] = 1
                        self._opt_dict['lang_cols'] = 0
                    else:
                        self._opt_dict['lang_rows'] = int(self._ui._file_portion_box.value()) + 1
                        self._opt_dict['lang_cols'] = 1

                elif 'zh' in lang_seq_dict.keys():
                    if count_col_en == 1:
                        title = "无标题"
                    else:
                        title = '有标题'
                    col_sent_list = []
                    col_id = lang_seq_dict['zh']
                    for item in tab_list:
                        col_sent_list.append(item[col_id])
                    lang_status, lang_gap = self.detect_lang_swap(col_sent_list)
                    self._ui._file_portion_box.setValue(lang_gap)
                    self._opt_dict['lang_cols'] = lang_gap
                    if lang_status == '双语分离':
                        self._opt_dict['lang_rows'] = 1
                        self._opt_dict['lang_cols'] = 0
                    else:
                        self._opt_dict['lang_rows'] = int(self._ui._file_portion_box.value()) + 1
                        self._opt_dict['lang_cols'] = 1
                else:
                    title = ''
                    lang_status = ''
                    lang_gap = ''

                pos_index = lang_status_dict[lang_status]
                self._ui._file_pos_box.setCurrentIndex(pos_index)
                self._opt_dict['lang_pos'] = lang_status
                self._ui._file_portion_box.setValue(lang_gap)
                self._opt_dict['lang_cols'] = lang_gap
                # 输出报告
                if count_col_num == 0:
                    num = "无行号"
                    marker_id_status = 0
                    self._ui._file_num_mark_box.setChecked(False)
                    self._opt_dict['marker_id'] = 0
                else:
                    num = "有行号"
                    marker_id_status = 1
                    self._ui._file_num_mark_box.setChecked(True)
                    self._opt_dict['marker_id'] = 1
                if title == "无标题":
                    marker_chapter = 0
                    self._ui._file_chapt_num_box.setChecked(False)
                    self._opt_dict['marker_chapt'] = 0
                else:
                    marker_chapter = 1
                    self._ui._file_chapt_num_box.setChecked(True)
                    self._opt_dict['marker_chapt'] = 1

            else:
                marker_id_status = -1
                marker_chapter = -1
                row_max = -1
                col_max = -1

            self._temp_list.clear()
            file_pos = self._opt_dict['lang_pos']
            row_max = self._opt_dict['lang_rows']
            if file_pos in ['英上中下', '英左中右', '中上英下', '中左英右', '双语分离'] and col_max >= 1:
                if file_pos in ['英上中下', '中上英下']:
                    col_max = self._opt_dict['marker_id'] + self._opt_dict['marker_chapt'] + self._opt_dict['lang_cols']
                    self.prepare_return_bi_list(marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list)
                elif file_pos in ['英左中右', '中左英右'] and col_max >= 2:
                    if self._opt_dict['marker_chapt'] == 0:
                        col_max = self._opt_dict['marker_id'] + self._opt_dict['lang_cols'] + 1
                    elif self._opt_dict['marker_chapt'] == 1:
                        col_max = self._opt_dict['marker_id'] + (self._opt_dict['lang_cols'] + 1) * 2
                    else:
                        col_max = 0
                    self.prepare_tab_bi_list(marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list)
                elif file_pos == "双语分离":
                    pass
                else:
                    self._ui._set_status_text("文件读取出现异常，请检查参数设置是否与语料一致！")
            else:
                pass

    # opt_organizer_group
    def opt_checker(self):
        file_dict = {}
        file_dict['file_path'] = self._ui._file_openBox.text()
        file_dict['file_type'] = self._ui._file_type_box.currentText()
        file_dict['file_bind'] = self._ui._file_bind_box.currentText()
        file_dict['file_num'] = int(self._ui._file_num_box.value())
        file_dict['lang_pos'] = self._ui._file_pos_box.currentText()
        if file_dict['lang_pos'] in ['英上中下', '中上英下']:
            file_dict['lang_rows'] = int(self._ui._file_portion_box.value()) + 1
            file_dict['lang_cols'] = 1
        elif file_dict['lang_pos'] in ['英左中右', '中左英右']:
            file_dict['lang_cols'] = int(self._ui._file_portion_box.value())
            file_dict['lang_rows'] = 1
        else:
            file_dict['lang_cols'] = -1
            file_dict['lang_rows'] = -1
        if self._ui._file_num_mark_box.isChecked():
            file_dict['marker_id'] = 1
        else:
            file_dict['marker_id'] = 0
        if self._ui._file_chapt_num_box.isChecked():
            file_dict['marker_chapt'] = 1
        else:
            file_dict['marker_chapt'] = 0
        if self._ui._file_tab_mark_box.isChecked():
            file_dict['marker_tab'] = 1
        else:
            file_dict['marker_tab'] = 0
        if self._ui._file_cuc_mark_box.isChecked():
            file_dict['marker_seg'] = 1
        else:
            file_dict['marker_seg'] = 0
        if self._ui._file_table_mark_box.isChecked():
            file_dict['marker_table'] = 1
        else:
            file_dict['marker_table'] = 0

        return file_dict

    # para_list_output_group
    def prepare_seperate_bi_list(self, en_para_list, zh_para_list):
        if self._opt_dict['marker_id'] == 1 and self._opt_dict['marker_chapt'] == 1:
            en_num_list = [x.split('\t')[0] for x in en_para_list]
            en_sent_list = [x.split('\t')[1] for x in en_para_list]
            en_chapter_list = [x.split('\t')[2] for x in en_para_list]
            zh_num_list = [x.split('\t')[0] for x in zh_para_list[0]]
            zh_sent_list = [x.split('\t')[1] for x in zh_para_list[0]]
            zh_chapter_list = [x.split('\t')[2] for x in zh_para_list[0]]
        elif self._opt_dict['marker_id'] == 1:
            en_num_list = [x.split('\t')[0] for x in en_para_list]
            en_sent_list = [x.split('\t')[1] for x in en_para_list]
            en_chapter_list = []
            zh_num_list = [x.split('\t')[0] for x in zh_para_list[0]]
            zh_sent_list = [x.split('\t')[1] for x in zh_para_list[0]]
            zh_chapter_list = []
        elif self._opt_dict['marker_chapt'] == 1:
            en_num_list = []
            en_sent_list = [x.split('\t')[0] for x in en_para_list]
            en_chapter_list = [x.split('\t')[1] for x in en_para_list]
            zh_num_list = []
            zh_sent_list = [x.split('\t')[0] for x in zh_para_list[0]]
            zh_chapter_list = [x.split('\t')[1] for x in zh_para_list[0]]
        else:
            en_num_list = []
            en_sent_list = [x.split('\t')[1] for x in en_para_list]
            en_chapter_list = []
            zh_num_list = []
            zh_sent_list = [x.split('\t')[1] for x in zh_para_list[0]]
            zh_chapter_list = []
        if en_sent_list:
            tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
            tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)

        else:
            tmp_en_title = ''
            tmp_en_author = ''
            tmp_en_translator = ''
            tmp_en_date = ''
            tmp_zh_title = ''
            tmp_zh_author = ''
            tmp_zh_translator = ''
            tmp_zh_date = ''
        if tmp_en_title:
            self._ui._ss_book_titleBox.setText(tmp_en_title)
            self._ui._ss_book_authorBox.setText(tmp_en_author)
            self._ui._ss_book_translatorBox.setText(tmp_en_translator)
            self._ui._ss_book_dateBox.setText(tmp_en_date)
            self._ui._ss_book_genreBox.setText('fairy tale')
            en_text = "\n".join(en_para_list)
            en_text = en_text.replace('ZZZZZ.', '')
            self._ui._ss_book_contentsBox.setText(en_text)
            self._ui._tt_book_titleBox.setText(tmp_zh_title)
            self._ui._tt_book_authorBox.setText(tmp_zh_author)
            self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
            self._ui._tt_book_dateBox.setText(tmp_zh_date)
            self._ui._tt_book_genreBox.setText('童话')
            zh_text = "\n".join(zh_para_list[0])
            self._ui._tt_book_contentsBox.setText(zh_text)
            self._ui._promptBox.setText(self._ui._prompt_2)
        else:
            self._ui._set_status_text('文件读取失败，请正确选择标记项')

    # para_list_output_group
    def prepare_return_bi_list(self, marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list):
        for num in range(row_max):
            sep_list = [item for item in para_list[num::row_max]]
            self._temp_list.append(sep_list)

        if marker_id_status == 1:
            if file_pos == '英上中下':
                for item in self._temp_list[0]:
                    self._current_en_para_list.append(item.replace('ZZZZZ.', ''))
                for item in self._temp_list[1:]:
                    self._current_zh_para_list.append(item)
            elif file_pos == '中上英下':
                for item in self._temp_list[0]:
                    self._current_zh_para_list.append(item)
                for item in self._temp_list[1:]:
                    self._current_en_para_list.append(item.replace('ZZZZZ.', ''))
            if col_max == 2:
                en_num_list = [x.split('\t')[0] for x in self._current_en_para_list]
                en_sent_list = [x.split('\t')[1] for x in self._current_en_para_list]
                zh_num_list = [x.split('\t')[0] for x in self._current_zh_para_list[0]]
                zh_sent_list = [x.split('\t')[1] for x in self._current_zh_para_list[0]]
                tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
            elif col_max == 3:
                en_num_list = [x.split('\t')[0] for x in self._current_en_para_list]
                en_sent_list = [x.split('\t')[1] for x in self._current_en_para_list]
                en_chapter_list = [x.split('\t')[2] for x in self._current_en_para_list]
                tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                zh_num_list = [x.split('\t')[0] for x in self._current_zh_para_list[0]]
                zh_sent_list = [x.split('\t')[1] for x in self._current_zh_para_list[0]]
                zh_chapter_list = [x.split('\t')[2] for x in self._current_zh_para_list[0]]
                tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
            else:
                tmp_en_title = ''
                tmp_en_author = ''
                tmp_en_translator = ''
                tmp_en_date = ''
                tmp_zh_title = ''
                tmp_zh_author = ''
                tmp_zh_translator = ''
                tmp_zh_date = ''
            if tmp_en_title:
                self._ui._ss_book_titleBox.setText(tmp_en_title)
                self._ui._ss_book_authorBox.setText(tmp_en_author)
                self._ui._ss_book_translatorBox.setText(tmp_en_translator)
                self._ui._ss_book_dateBox.setText(tmp_en_date)
                self._ui._ss_book_genreBox.setText('fairy tale')
                en_text = "\n".join(self._current_en_para_list)
                en_text = en_text.replace('ZZZZZ.', '')
                self._ui._ss_book_contentsBox.setText(en_text)
                self._ui._tt_book_titleBox.setText(tmp_zh_title)
                self._ui._tt_book_authorBox.setText(tmp_zh_author)
                self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
                self._ui._tt_book_dateBox.setText(tmp_zh_date)
                self._ui._tt_book_genreBox.setText('童话')
                zh_text = "\n".join(self._current_zh_para_list[0])
                self._ui._tt_book_contentsBox.setText(zh_text)
                self._ui._promptBox.setText(self._ui._prompt_2)
            else:
                self._ui._set_status_text('文件读取失败，请正确选择标记项')
        else:
            if file_pos == '英上中下':
                for item in self._temp_list[0]:
                    self._current_en_para_list.append(item.replace('ZZZZZ.', ''))
                for item in self._temp_list[1:]:
                    self._current_zh_para_list.append(item)
            elif file_pos == '中上英下':
                for item in self._temp_list[0]:
                    self._current_zh_para_list.append(item)
                for item in self._temp_list[1:]:
                    self._current_en_para_list.append(item.replace('ZZZZZ.', ''))
            if col_max == 1:
                tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(self._current_en_para_list)
                tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(
                    self._current_zh_para_list[0])
            elif col_max == 2:
                en_sent_list = [x.split('\t')[0] for x in self._current_en_para_list]
                en_chapter_list = [x.split('\t')[1] for x in self._current_en_para_list]
                zh_sent_list = [x.split('\t')[0] for x in self._current_zh_para_list[0]]
                zh_chapter_list = [x.split('\t')[1] for x in self._current_zh_para_list[0]]
                tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
            else:
                tmp_en_title = ''
                tmp_en_author = ''
                tmp_en_translator = ''
                tmp_en_date = ''
                tmp_zh_title = ''
                tmp_zh_author = ''
                tmp_zh_translator = ''
                tmp_zh_date = ''
            if tmp_en_title:
                self._ui._ss_book_titleBox.setText(tmp_en_title)
                self._ui._ss_book_authorBox.setText(tmp_en_author)
                self._ui._ss_book_translatorBox.setText(tmp_en_translator)
                self._ui._ss_book_dateBox.setText(tmp_en_date)
                self._ui._ss_book_genreBox.setText('fairy tale')
                self._ui._ss_book_contentsBox.setText(
                    "\n".join([x[:50] + "..." if len(x) > 50 else x for x in self._current_en_para_list]))
                self._ui._tt_book_titleBox.setText(tmp_zh_title)
                self._ui._tt_book_authorBox.setText(tmp_zh_author)
                self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
                self._ui._tt_book_dateBox.setText(tmp_zh_date)
                self._ui._tt_book_genreBox.setText('童话')
                self._ui._tt_book_contentsBox.setText(
                    "\n".join([y[:25] + "..." if len(y) > 25 else y for y in self._current_zh_para_list[0]]))
                self._ui._promptBox.setText(self._ui._prompt_2)
            else:
                self._ui._set_status_text('文件读取失败，请正确选择标记项')

    # para_list_output_group
    def prepare_tab_bi_list(self, marker_id_status, marker_chapter, file_pos, row_max, col_max, para_list):
        # 路径：有行号(无标题|有标题)|无行号(无标题|有标题)
        # 按总列数组织临时列表[[列0],[列1]...]
        for num in range(col_max):
            sep_list = [item.split('\t')[num].replace("ZZZZZ.", "") for item in para_list]
            self._temp_list.append(sep_list)
        # 如果有行号，列0为行号
        if self._opt_dict['marker_id'] == 1:
            # 总列数为3或4时，不可能含篇章标题，列1,列2，列3为英、汉，汉，生成[序号,语1]两列英文段落列表与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
            if 3 <= col_max <= 4:
                if file_pos == '英左中右':
                    self._current_en_para_list.extend(
                        list(zip(self._temp_list[0], self._temp_list[1])))  # zip一定要转成列表，否则深层数据提出不出来
                    i = 2
                    while i < col_max:
                        self._current_zh_para_list.append(list(zip(self._temp_list[0], self._temp_list[i])))
                        i += 1
                elif file_pos == '中左英右':
                    self._current_zh_para_list.extend(list(zip(self._temp_list[0], self._temp_list[1])))
                    i = 2
                    while i < col_max:
                        self._current_en_para_list.append(list(zip(self._temp_list[0], self._temp_list[i])))
                        i += 1
                else:
                    self._current_en_para_list = []
                    self._current_zh_para_list = []

            # 总列数大于等于5时，可能含标题
            elif col_max >= 5:
                # 有篇章标题时，列1,英，列2，标题，列3，中1，列4，标题....
                if marker_chapter == 1:
                    if file_pos == '英左中右':
                        self._current_en_para_list.extend(
                            list(zip(self._temp_list[0], self._temp_list[1], self._temp_list[2])))
                        i = 3
                        while i < col_max:
                            j = i + 1
                            self._current_zh_para_list.append(
                                list(zip(self._temp_list[0], self._temp_list[i], self._temp_list[j])))
                            i = j
                            i += 1
                    elif file_pos == '中左英右':
                        self._current_zh_para_list.extend(
                            list(zip(self._temp_list[0], self._temp_list[1], self._temp_list[2])))
                        i = 3
                        while i < col_max:
                            j = i + 1
                            self._current_en_para_list.append(
                                list(zip(self._temp_list[0], self._temp_list[i], self._temp_list[j])))
                            i = j
                            i += 1
                    else:
                        self._current_en_para_list.clear()
                        self._current_zh_para_list.clear()
                else:
                    # 无篇章标题时，列1,列2，列3...为英，汉，汉...生成[序号,语1]两列英文段落列表
                    # 与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
                    if file_pos == '英左中右':
                        self._current_en_para_list.extend(
                            list(zip(self._temp_list[0], self._temp_list[1])))  # zip一定要转成列表，否则深层数据提出不出来
                        i = 2
                        while i < col_max:
                            self._current_zh_para_list.append(list(zip(self._temp_list[0], self._temp_list[i])))
                            i += 1
                    elif file_pos == '中左英右':
                        self._current_zh_para_list.extend(list(zip(self._temp_list[0], self._temp_list[1])))
                        i = 2
                        while i < col_max:
                            self._current_en_para_list.append(list(zip(self._temp_list[0], self._temp_list[i])))
                            i += 1
                    else:
                        self._current_en_para_list = []
                        self._current_zh_para_list = []
            else:
                self._current_en_para_list.clear()
                self._current_zh_para_list.clear()

            if self._current_en_para_list == []:
                self._ui._set_status_text('文件读取失败，请核实文本的具体列数')
                tmp_en_title = ''
                tmp_en_author = ''
                tmp_en_translator = ''
                tmp_en_date = ''
                tmp_zh_title = ''
                tmp_zh_author = ''
                tmp_zh_translator = ''
                tmp_zh_date = ''
            else:
                if marker_chapter == 0:
                    en_num_list = [x for (x, y) in self._current_en_para_list]
                    en_sent_list = [y for (x, y) in self._current_en_para_list]
                    tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                    zh_num_list = [x for (x, y) in self._current_zh_para_list[0]]
                    zh_sent_list = [y for (x, y) in self._current_zh_para_list[0]]
                    try:
                        tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
                    except:
                        self._ui._set_status_text('中文信息提取失败！')
                        tmp_zh_title = ''
                        tmp_zh_author = ''
                        tmp_zh_translator = ''
                        tmp_zh_date = ''
                else:
                    en_num_list = [x for (x, y, z) in self._current_en_para_list]
                    en_sent_list = [y for (x, y, z) in self._current_en_para_list]
                    en_chapter_list = [z for (x, y, z) in self._current_en_para_list]
                    tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                    zh_num_list = [x for (x, y, z) in self._current_zh_para_list[0]]
                    zh_sent_list = [y for (x, y, z) in self._current_zh_para_list[0]]
                    zh_chapter_list = [z for (x, y, z) in self._current_zh_para_list[0]]
                    try:
                        tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
                    except:
                        self._ui._set_status_text('中文信息提取失败！')
                        tmp_zh_title = ''
                        tmp_zh_author = ''
                        tmp_zh_translator = ''
                        tmp_zh_date = ''
            if tmp_en_title:
                self._ui._ss_book_titleBox.setText(tmp_en_title)
                self._ui._ss_book_authorBox.setText(tmp_en_author)
                self._ui._ss_book_dateBox.setText(tmp_en_date)
                self._ui._ss_book_genreBox.setText('fairy tale')
                print_en_para_list = []
                for item in self._current_en_para_list:
                    item_line = len(item)
                    if item_line == 2:
                        print_en_para_list.append(item[0] + "\t" + item[1])
                    elif item_line == 3:
                        print_en_para_list.append(item[0] + "\t" + item[1] + "\t" + item[2])
                    else:
                        print_en_para_list = ""
                en_text = "\n".join(print_en_para_list)
                en_text = en_text.replace('ZZZZZ.', '')
                self._ui._ss_book_contentsBox.setText(en_text)
                self._ui._tt_book_titleBox.setText(tmp_zh_title)
                self._ui._tt_book_authorBox.setText(tmp_zh_author)
                self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
                self._ui._tt_book_dateBox.setText(tmp_zh_date)
                self._ui._tt_book_genreBox.setText('童话')
                print_zh_para_list = []
                for item in self._current_zh_para_list[0]:
                    item_line = len(item)
                    if item_line == 2:
                        print_zh_para_list.append(item[0] + "\t" + item[1])
                    elif item_line == 3:
                        print_zh_para_list.append(item[0] + "\t" + item[1] + "\t" + item[2])
                    else:
                        print_zh_para_list = ""
                zh_text = "\n".join(print_zh_para_list)
                self._ui._tt_book_contentsBox.setText(zh_text)
                self._ui._promptBox.setText(self._ui._prompt_2)
            else:
                self._ui._set_status_text('文件读取失败，请正确选择标记项')
        else:
            # 无篇章标题：列0英，列1中，列2中...
            # 有篇章标题：列0英，列1英标题，列2中,列3中标题，列4中，列5中标题
            # 总列数为2或3时，不可能含篇章标题，列0,列1，列2为英、汉，汉，生成[序号,语1]两列英文段落列表与[[序号,语1][序号,语1]...]两列嵌套中文段落列表
            if 2 <= col_max <= 3:
                if file_pos == '英左中右':
                    self._current_en_para_list.extend(self._temp_list[0])
                    i = 1
                    while i < col_max:
                        self._current_zh_para_list.append(self._temp_list[i])
                        i += 1
                elif file_pos == '中左英右':
                    self._current_zh_para_list.extend(self._temp_list[0])
                    i = 1
                    while i < col_max:
                        self._current_en_para_list.append(self._temp_list[i])
                        i += 1
                else:
                    self._current_en_para_list = []
                    self._current_zh_para_list = []

            # 总列数大于等于4时，可能含标题
            elif col_max >= 4:
                # 有篇章标题时，列0,英，列1，英标题，列2，中，列3，中标题....
                if marker_chapter == 1:
                    if file_pos == '英左中右':
                        self._current_en_para_list.extend(list(zip(self._temp_list[0], self._temp_list[1])))
                        i = 2
                        while i < col_max:
                            j = i + 1
                            self._current_zh_para_list.append(list(zip(self._temp_list[i], self._temp_list[j])))
                            i = j
                            i += 1
                    elif file_pos == '中左英右':
                        self._current_zh_para_list.extend(list(zip(self._temp_list[0], self._temp_list[1])))
                        i = 2
                        while i < col_max:
                            j = i + 1
                            self._current_en_para_list.append(list(zip(self._temp_list[i], self._temp_list[j])))
                            i = j
                            i += 1
                    else:
                        self._current_en_para_list.clear()
                        self._current_zh_para_list.clear()
                else:
                    # 无篇章标题时，列0,英,列1,汉,列2，汉
                    if file_pos == '英左中右':
                        self._current_en_para_list.extend(self._temp_list[0])  # zip一定要转成列表，否则深层数据提出不出来
                        i = 1
                        while i < col_max:
                            self._current_zh_para_list.append(self._temp_list[i])
                            i += 1
                    elif file_pos == '中左英右':
                        self._current_zh_para_list.extend(self._temp_list[0])
                        i = 2
                        while i < col_max:
                            self._current_en_para_list.append(self._temp_list[i])
                            i += 1
                    else:
                        self._current_en_para_list = []
                        self._current_zh_para_list = []
            else:
                self._current_en_para_list.clear()
                self._current_zh_para_list.clear()
            if self._current_en_para_list == []:
                self._ui._set_status_text('文件读取失败，请核实文本的具体列数')
                tmp_en_title = ''
                tmp_en_author = ''
                tmp_en_translator = ''
                tmp_en_date = ''
                tmp_zh_title = ''
                tmp_zh_author = ''
                tmp_zh_translator = ''
                tmp_zh_date = ''
            else:
                if marker_chapter == 1:
                    en_sent_list = [x for (x, y) in self._current_en_para_list]
                    en_chapter_list = [y for (x, y) in self._current_en_para_list]
                    tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                    zh_sent_list = [x for (x, y) in self._current_zh_para_list[0]]
                    zh_chapter_list = [y for (x, y) in self._current_zh_para_list[0]]
                    try:
                        tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
                    except:
                        self._ui._set_status_text('中文信息提取失败！')
                        tmp_zh_title = ''
                        tmp_zh_author = ''
                        tmp_zh_translator = ''
                        tmp_zh_date = ''
                else:
                    en_sent_list = self._current_en_para_list
                    tmp_en_title, tmp_en_author, tmp_en_translator,tmp_en_date = self._info_collector.info_collector_en(en_sent_list)
                    zh_sent_list = self._current_zh_para_list[0]
                    try:
                        tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(zh_sent_list)
                    except:
                        self._ui._set_status_text('中文信息提取失败！')
                        tmp_zh_title = ''
                        tmp_zh_author = ''
                        tmp_zh_translator = ''
                        tmp_zh_date = ''
            if tmp_en_title:
                self._ui._ss_book_titleBox.setText(tmp_en_title)
                self._ui._ss_book_authorBox.setText(tmp_en_author)
                self._ui._ss_book_dateBox.setText(tmp_en_date)
                self._ui._ss_book_genreBox.setText('fairy tale')
                print_en_para_list = []
                if marker_chapter == 1:
                    for item in self._current_en_para_list:
                        print_en_para_list.append(item[0] + "\t" + item[1])
                else:
                    print_en_para_list = self._current_en_para_list
                en_text = "\n".join(print_en_para_list)
                en_text = en_text.replace('ZZZZZ.', '')
                self._ui._ss_book_contentsBox.setText(en_text)
                self._ui._tt_book_titleBox.setText(tmp_zh_title)
                self._ui._tt_book_authorBox.setText(tmp_zh_author)
                self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
                self._ui._tt_book_dateBox.setText(tmp_zh_date)
                self._ui._tt_book_genreBox.setText('童话')
                print_zh_para_list = []
                if marker_chapter == 1:
                    for item in self._current_zh_para_list[0]:
                        print_zh_para_list.append(item[0] + "\t" + item[1])
                else:
                    print_zh_para_list = self._current_zh_para_list[0]
                zh_text = "\n".join(print_zh_para_list)
                self._ui._tt_book_contentsBox.setText(zh_text)
                self._ui._promptBox.setText(self._ui._prompt_2)
            else:
                self._ui._set_status_text('文件读取失败，请正确选择标记项')

    # auto_filler_group
    def json_en_filler(self):
        self._current_en_chapter_num_list.clear()
        alert_msg = []
        if self._ui._file_openBox.text() == "":
            alert_msg.append('正文')
        if self._ui._ss_book_titleBox.text() == "":
            alert_msg.append('书名')
        if self._ui._ss_book_authorBox.text() == "":
            alert_msg.append('作者')
        if self._ui._ss_book_genreBox.text() == "":
            alert_msg.append('体裁')
        if alert_msg:
            alert_msg = "、".join(alert_msg)
            alert_detail = "源语" + alert_msg + "项不能为空！"
            self._ui._set_status_text(alert_detail)
        else:
            title = self._ui._ss_book_titleBox.text()
            self._current_dict_key = title.strip()
            self._current_dict_key = re.sub(r'\s+', '', self._current_dict_key)
            author = self._ui._ss_book_authorBox.text()
            translator = ''
            language = self._ui._ss_book_languageBox.text()
            date = self._ui._ss_book_dateBox.text()
            genre = self._ui._ss_book_genreBox.text()
            version = self._ui._ss_book_versionBox.text()
            self._current_en_dict_version = version
            current_en_text = self._ui._ss_book_contentsBox.toPlainText()
            current_en_text_list = current_en_text.split('\n')
            line_sample = current_en_text_list[0]
            line_part = line_sample.split('\t')
            col_count = len(line_part)
            if col_count == 1:
                temp_num_list = []
                temp_sent_list = current_en_text_list
                temp_chapter_list = []
            elif col_count == 2:
                if line_sample[0].isdigit() == True:
                    temp_num_list = [sent.split('\t')[0] for sent in current_en_text_list]
                    temp_sent_list = [sent.split('\t')[1] for sent in current_en_text_list]
                    temp_chapter_list = []
                else:
                    temp_num_list = []
                    temp_sent_list = [sent.split('\t')[0] for sent in current_en_text_list]
                    temp_chapter_list = [sent.split('\t')[1] for sent in current_en_text_list]
            else:
                temp_num_list = [sent.split('\t')[0] for sent in current_en_text_list]
                temp_sent_list = [sent.split('\t')[1] for sent in current_en_text_list]
                temp_chapter_list = [sent.split('\t')[2] for sent in current_en_text_list]

            if temp_num_list == [] and temp_chapter_list == []:
                new_sent_list, new_chapter_list, en_chpt_num_list = self._chapter_maker.add_chapter(temp_sent_list)
                en_contents = [str(num) + "\t" + para + "\t" + chapter for num, (para, chapter) in
                               enumerate(zip(new_sent_list, new_chapter_list), start = 1)]
                en_contents_shown = [str(num) + " ¦ " + para + ' ¦ ' + chapter for num, (para, chapter) in
                                     enumerate(zip(new_sent_list, new_chapter_list), start = 1)]
                self._current_en_chapter_num_list = en_chpt_num_list
            elif temp_num_list == []:
                en_contents = [str(num) + '\t' + sent + '\t' + chapter for num, (sent, chapter) in
                               enumerate(zip(temp_sent_list, temp_chapter_list), start = 1)]
                en_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, (sent, chapter) in
                                     enumerate(zip(temp_sent_list, temp_chapter_list), start = 1)]
                self._current_en_chapter_num_list = []
            elif temp_chapter_list == []:
                new_sent_list, new_chapter_list, en_chpt_num_list = self._chapter_maker.add_chapter(temp_sent_list)
                en_contents = [str(num) + '\t' + sent + '\t' + chapter for num, sent, chapter in
                               zip(temp_num_list, new_sent_list, new_chapter_list)]
                en_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, sent, chapter in
                                     zip(temp_num_list, new_sent_list, new_chapter_list)]
                self._current_en_chapter_num_list = en_chpt_num_list
            else:
                en_contents = [str(num) + '\t' + sent + '\t' + chapter for num, sent, chapter in
                               zip(temp_num_list, temp_sent_list, temp_chapter_list)]
                en_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, sent, chapter in
                                     zip(temp_num_list, temp_sent_list, temp_chapter_list)]
                self._current_en_chapter_num_list = []

            self._ui._ss_book_contentsBox.clear()
            self._ui._ss_book_contentsBox.setText("\n".join(en_contents_shown))
            self._en_bookDict.clear()
            self._en_bookDict['title'] = title
            self._en_bookDict['author'] = author
            self._en_bookDict['translator'] = translator
            self._en_bookDict['language'] = language
            self._en_bookDict['date'] = date
            self._en_bookDict['genre'] = genre
            self._en_bookDict['content'] = defaultdict(str)
            for line in en_contents:
                line = line.split('\t')
                num = line[0]
                para = line[1]
                chapt = line[2]
                self._en_bookDict['content'][num] = para + '\t' + chapt

            self._ui._ss_book_uploadButton.setEnabled(False)
            self._ui._tt_book_uploadButton.setEnabled(True)
            self._ui._ss_book_redoButton.setEnabled(True)
            self._ui._promptBox.setText(self._ui._prompt_3)

        return self._current_dict_key, self._current_en_dict_version, self._current_en_chapter_num_list

    # auto_filler_group
    def json_zh_filler(self):
        alert_msg = []
        if self._ui._file_openBox.text() == "":
            alert_msg.append('正文')
        if self._ui._tt_book_titleBox.text() == "":
            alert_msg.append('书名')
        if self._ui._tt_book_translatorBox.text() == "":
            alert_msg.append('译者')
        if self._ui._tt_book_genreBox.text() == "":
            alert_msg.append('体裁')
        if alert_msg:
            alert_msg = "、".join(alert_msg)
            alert_detail = "目标语" + alert_msg + "项不能为空！"
            self._ui._set_status_text(alert_detail)
        else:
            title = self._ui._tt_book_titleBox.text()
            author = self._ui._tt_book_authorBox.text()
            translator = self._ui._tt_book_translatorBox.text()
            language = self._ui._tt_book_languageBox.text()
            date = self._ui._tt_book_dateBox.text()
            genre = self._ui._tt_book_genreBox.text()
            version = self._ui._tt_book_versionBox.text()
            self._current_zh_dict_version = version
            book_id = title
            chapter = title.strip()
            version_count = len(self._current_zh_para_list)
            zh_vn = int(version.replace("t", ""))

            if zh_vn < version_count:
                self._ui._tt_book_nextButton.setEnabled(True)
            else:
                self._ui._tt_book_nextButton.setEnabled(False)
                self._ui._tt_book_uploadButton.setEnabled(False)

            current_zh_text_list = self._current_zh_para_list[zh_vn - 1]
            line_sample = current_zh_text_list[0]

            # 列表内容如果是元组：
            if isinstance(line_sample, tuple) == True:
                # 统计元组元素个数用len方法
                col_count = len(line_sample)
                if col_count == 1:
                    temp_num_list = []
                    temp_sent_list = [x for x in current_zh_text_list if x != '']
                    temp_chapter_list = []
                elif col_count == 2:
                    if line_sample[0].isdigit() == True:
                        temp_num_list = [sent[0] for sent in current_zh_text_list if sent[1] != '']
                        temp_sent_list = [sent[1] for sent in current_zh_text_list if sent[1] != '']
                        temp_chapter_list = []
                    else:
                        temp_num_list = []
                        temp_sent_list = [sent[0] for sent in current_zh_text_list if sent[0] != '']
                        temp_chapter_list = [sent[1] for sent in current_zh_text_list if sent[1] != '']
                else:
                    temp_num_list = [sent[0] for sent in current_zh_text_list if sent[1] != '']
                    temp_sent_list = [sent[1] for sent in current_zh_text_list if sent[1] != '']
                    temp_chapter_list = [sent[2] for sent in current_zh_text_list if sent[2] != '']
            # 否则为字符串：
            else:
                col_count = len(line_sample.split('\t'))
                if col_count == 1:
                    temp_num_list = []
                    temp_sent_list = [x for x in current_zh_text_list if x != '']
                    temp_chapter_list = []
                elif col_count == 2:
                    if line_sample[0].isdigit() == True:
                        temp_num_list = [sent.split('\t')[0] for sent in current_zh_text_list if
                                         sent.split('\t')[1] != '']
                        temp_sent_list = [sent.split('\t')[1] for sent in current_zh_text_list if
                                          sent.split('\t')[1] != '']
                        temp_chapter_list = []
                    else:
                        temp_num_list = []
                        temp_sent_list = [sent.split('\t')[0] for sent in current_zh_text_list if
                                          sent.split('\t')[0] != '']
                        temp_chapter_list = [sent.split('\t')[1] for sent in current_zh_text_list if
                                             sent.split('\t')[1] != '']
                else:
                    temp_num_list = [sent.split('\t')[0] for sent in current_zh_text_list if sent.split('\t')[1] != '']
                    temp_sent_list = [sent.split('\t')[1] for sent in current_zh_text_list if sent.split('\t')[1] != '']
                    temp_chapter_list = [sent.split('\t')[2] for sent in current_zh_text_list if
                                         sent.split('\t')[2] != '']

            if temp_num_list == [] and temp_chapter_list == []:
                temp_num_list = [num for num, sent in enumerate(temp_sent_list, start = 1)]
                temp_sent_chapter_list = self.swap_chapter(zip(temp_num_list, temp_sent_list),
                                                           self._current_en_chapter_num_list)
                zh_contents = [str(num) + "\t" + para + "\t" + chapter for num, (para, chapter) in
                               zip(temp_num_list, temp_sent_chapter_list)]
                zh_contents_shown = [str(num) + " ¦ " + para + ' ¦ ' + chapter for num, (para, chapter) in
                                     zip(temp_num_list, temp_sent_chapter_list)]
            elif temp_num_list == []:
                zh_contents = [str(num) + '\t' + sent + '\t' + chapter for num, (sent, chapter) in
                               enumerate(zip(temp_sent_list, temp_chapter_list), start = 1)]
                zh_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, (sent, chapter) in
                                     enumerate(zip(temp_sent_list, temp_chapter_list), start = 1)]
            elif temp_chapter_list == []:

                temp_sent_chapter_list = self.swap_chapter(zip(temp_num_list, temp_sent_list),
                                                           self._current_en_chapter_num_list)
                zh_contents = [str(num) + '\t' + sent + '\t' + chapter for num, (sent, chapter) in
                               zip(temp_num_list, temp_sent_chapter_list)]
                zh_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, (sent, chapter) in
                                     zip(temp_num_list, temp_sent_chapter_list)]
            else:
                zh_contents = [str(num) + '\t' + sent + '\t' + chapter for num, sent, chapter in
                               zip(temp_num_list, temp_sent_list, temp_chapter_list)]
                zh_contents_shown = [str(num) + " ¦ " + sent + ' ¦ ' + chapter for num, sent, chapter in
                                     zip(temp_num_list, temp_sent_list, temp_chapter_list)]
            self._ui._tt_book_contentsBox.clear()
            self._ui._tt_book_contentsBox.setText("\n".join(zh_contents_shown))
            zh_bookDict = {}
            zh_bookDict['title'] = title
            zh_bookDict['author'] = author
            zh_bookDict['translator'] = translator
            zh_bookDict['language'] = language
            zh_bookDict['date'] = date
            zh_bookDict['genre'] = genre
            zh_bookDict['content'] = defaultdict(str)
            for line in zh_contents:
                line = line.split('\t')
                num = line[0]
                para = line[1]
                chapt = line[2]
                zh_bookDict['content'][num] = para + '\t' + chapt
            self._zh_bookDict_list.append(zh_bookDict)
            self._ui._tt_book_redoButton.setEnabled(True)
            self._ui._tt_book_uploadButton.setEnabled(False)
            self._ui._prompt_4 = f"目标语语料{self._current_zh_dict_version}提交成功，所有语料均已提交完毕。\n步骤4：请点击“转换格式”按钮生成一对多字典文件。"
            self._ui._prompt_4b = f"目标语语料{self._current_zh_dict_version}提交成功，尚有其他目标语语料等待添加。\n步骤4：请点击“下一译文”按钮继续添加余下目标语语料。"
            if self._ui._tt_book_nextButton.isEnabled() == False:
                self._ui._promptBox.setText(self._ui._prompt_4)
            else:
                self._ui._promptBox.setText(self._ui._prompt_4b)

        return self._current_zh_dict_version

    def option_reset(self):
        self._ui._file_openBox.clear()
        self._ui._file_type_box.setCurrentIndex(0)
        if self._current_file:
            self._ui._file_bind_box.setCurrentIndex(0)
        else:
            self._ui._file_bind_box.setCurrentIndex(1)
        self._ui._file_num_box.setValue(1)
        self._ui._file_portion_box.setValue(1)
        self._ui._file_pos_box.setCurrentIndex(0)
        self._ui._file_num_mark_box.setChecked(False)
        self._ui._file_chapt_num_box.setChecked(False)
        self._ui._file_tab_mark_box.setChecked(False)
        self._ui._file_cuc_mark_box.setChecked(False)
        self._ui._file_table_mark_box.setChecked(False)

    def form_reset(self):
        self._ui._ss_book_titleBox.clear()
        self._ui._tt_book_titleBox.clear()
        self._ui._ss_book_authorBox.clear()
        self._ui._tt_book_authorBox.clear()
        self._ui._tt_book_translatorBox.clear()
        self._ui._ss_book_genreBox.clear()
        self._ui._tt_book_genreBox.clear()
        self._ui._ss_book_dateBox.clear()
        self._ui._tt_book_dateBox.clear()
        self._ui._tt_book_versionBox.setText('t1')
        self._ui._ss_book_contentsBox.clear()
        self._ui._tt_book_contentsBox.clear()
        self._ui._ss_book_uploadButton.setEnabled(True)
        self._ui._tt_book_uploadButton.setEnabled(False)
        self._ui._ss_book_redoButton.setEnabled(False)
        self._ui._tt_book_redoButton.setEnabled(False)
        self._current_en_para_list.clear()
        self._current_zh_para_list.clear()
        self._en_bookDict = {}
        self._zh_bookDict_list.clear()
        self._temp_list.clear()

        return self._en_bookDict

    # auto_refiller_group
    def json_en_refiller(self):
        self._ui._ss_book_uploadButton.setEnabled(True)
        self._en_bookDict.clear()
        self._ui._ss_book_titleBox.clear()
        self._ui._ss_book_authorBox.clear()
        self._ui._ss_book_genreBox.clear()
        self._ui._ss_book_dateBox.clear()
        self._ui._ss_book_contentsBox.clear()
        self._current_en_dict_version = ""
        self._current_dict_key = ""
        if self._current_en_para_list:
            self._ui._ss_book_contentsBox.setText("\n".join(self._current_en_para_list))
        else:
            pass

        return self._current_dict_key, self._current_en_dict_version

    # auto_refiller_group
    def json_zh_refiller(self):
        self._ui._tt_book_uploadButton.setEnabled(True)
        self._zh_bookDict_list.clear()
        self._ui._tt_book_titleBox.clear()
        self._ui._tt_book_authorBox.clear()
        self._ui._tt_book_translatorBox.clear()
        self._ui._tt_book_genreBox.clear()
        self._ui._tt_book_versionBox.clear()
        self._ui._tt_book_versionBox.setText('t1')
        self._ui._tt_book_dateBox.clear()
        self._ui._tt_book_contentsBox.clear()
        if self._current_zh_para_list:
            self._ui._tt_book_contentsBox.setText("\n".join(self._current_zh_para_list[0]))
        else:
            pass
        self._current_zh_dict_version = 't1'
        return self._current_zh_dict_version

    # version_shift_group
    def load_next_version(self):
        version_count = len(self._current_zh_para_list)
        version_num = int(self._current_zh_dict_version.replace("t", ""))
        if version_num <= version_count:
            next_num = version_num + 1
        else:
            next_num = ""
        if next_num:
            self._ui._tt_book_versionBox.setText(f't{next_num}')
            self.json_zh_filler()
            temp_text = self._ui._tt_book_contentsBox.toPlainText()
            temp_text = temp_text.split('\n')
            temp_lines = [item.split('¦')[1] for item in temp_text[:3]]
            try:
                tmp_zh_title, tmp_zh_author, tmp_zh_translator, tmp_zh_date = self._info_collector.info_collector_zh(temp_lines)
                self._ui._tt_book_translatorBox.setText(tmp_zh_translator)
                self._ui._tt_book_dateBox.setText(tmp_zh_date)
                self._ui._prompt_4a = f"当前目标语语料版本号为t{next_num}，确认无误后，请点击“提交按钮”。"
                self._ui._promptBox.setText(self._ui._prompt_4a)
            except:
                self._ui._tt_book_translatorBox.clear()
                self._ui._tt_book_dateBox.clear()
            finally:
                self._ui._tt_book_uploadButton.setEnabled(True)
                self._ui._tt_book_nextButton.setEnabled(False)
        else:
            pass

    # auto_filler_group
    def swap_chapter(self, zh_num_sent_list, en_chapt_num_list):
        # print("start swap chapter")
        # 必须核实num类型是否为数字类型。
        chapter_list = []
        for num, sent in zh_num_sent_list:
            if isinstance(num, str):
                num = eval(num)
            else:
                pass
            if str(num - 1) in en_chapt_num_list:
                chapter_list.append('[T]' + sent)
            else:
                chapter_list.append(sent)
        temp_id = ''
        new_list = []
        for para in chapter_list:
            if para.startswith(r'[T]'):
                if para == chapter_list[0]:
                    # 去除标题行有可能存在的副标题
                    para = para.split(r'（')[0].strip()
                    para = para.split(r'——')[0].strip()
                else:
                    para = para.strip()
                temp_id = para.replace('[T]', '')
                new_list.append((para.replace('[T]', ''), temp_id))
            else:
                new_list.append((para.replace('[T]', ''), temp_id))
        return new_list

    # data_save_group
    def write_to_json(self):
        if self._en_bookDict and self._zh_bookDict_list:
            mydict = {}
            book_id = self._current_dict_key
            if book_id:
                en_version = self._current_en_dict_version
                zh_version = self._current_zh_dict_version
                mydict[book_id] = {}
                mydict[book_id]['en'] = {}
                mydict[book_id]['zh'] = {}
                mydict[book_id]['en'][en_version] = self._en_bookDict
                for i, zh_version_dict in enumerate(self._zh_bookDict_list, start = 1):
                    zn = "t" + str(i)
                    mydict[book_id]['zh'][zn] = zh_version_dict
                json_to_save = os.path.join(self._outPutDir, book_id + ".json")
                if mydict:
                    with open(json_to_save, mode = 'w', encoding = "utf-8-sig") as f:
                        json.dump(mydict, f)
                        self._ui._promptBox.setText(self._ui._prompt_5)
                else:
                    pass
            else:
                pass
        else:
            self._ui._set_status_text("很抱歉，英汉数据尚未创建，请按提示操作。")
