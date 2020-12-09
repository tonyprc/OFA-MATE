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

class ChapterFiller:
    def __int__(self):
        pass


    def _punc_loader(self,file):
        with open(file,'r',encoding = 'utf-8-sig') as f:
            punc_list = set([x.strip() for x in f.readlines()])
        return punc_list

    def _digit_loader(self,file_en,file_zh):
        with open(file_en,'r',encoding = 'utf-8-sig') as f:
            sent_list = [sent.strip() for sent in f.readlines()]
            digit_en_dict = {sent.split('\t')[0]:eval(sent.split('\t')[1]) for sent in sent_list}
        with open(file_zh,'r',encoding = 'utf-8-sig') as f:
            sent_list = [sent.strip() for sent in f.readlines()]
            digit_zh_dict = {sent.split('\t')[0]:sent.split('\t')[1] for sent in sent_list}
        return digit_en_dict,digit_zh_dict

    def _chapter_detector(self,sent,sent_end):
        current_dir = os.getcwd()
        data_dir = os.path.join(current_dir, 'app_data')
        punc_file = os.path.join(data_dir, 'workfiles', 'punc.dat')
        digit_en_file = os.path.join(data_dir, 'workfiles', 'digit_en.dat')
        digit_zh_file = os.path.join(data_dir, 'workfiles', 'digit_zh.dat')
        digit_en_dict,digit_zh_dict = self._digit_loader(digit_en_file,digit_zh_file)
        punc_filter_list = self._punc_loader(punc_file)

        chapt_len_sure = 0
        chapt_len_unsure = 0
        chapt_a = re.search(r'''^Section|^SECTION|^Part|^PART|^Chapter|^CHAPTER|^[ivxlcdmIIIVXLCDM]+$''',sent)
        chapt_b = re.search(r'''[^\,\.\:\"\'\*\^\#\$\@\!~\(\)\_\-\+\ = \{\}\[\]\?\/\<\>\&\%\;\\，。：、；“”’！…—（）《》｛｝【】？]$''',sent)
        s = sent.split()
        wd = s[0].lower()
           
        if chapt_a:
            result = 'on'
            if sent_end == ":":
               result = 'off'
        elif chapt_b:
            if sent_end == ":":
                result = 'off'
            else:
                if sent[-1] in punc_filter_list:
                   result = 'off'
                   #print("no for ending punc:",sent)
                elif sent.isdigit():
                    result = 'on'
                elif wd in digit_en_dict.keys():
                    result = 'on'
                    if len(sent) >= 100:
                        result = 'off'
                elif sent.istitle():
                    result = 'on'
                elif sent.isupper():
                    result = 'on'
                else:
                    result = 'off'
        else:
            result = 'off'

        sent_end = ''
        if sent[-1] == ":":
            sent_end = ':'

        return result,sent_end
        
    def add_chapter(self,para_list = []):
        sent_end = ""        
        new_sent_list = []
        new_chapter_list = []
        sl_chpt_num_list = []
        chapter_id = ''

        if para_list == []:
            pass
        else:        
            #默认第一行为标题行
            i = 2        
            chapter_id = para_list[0]
            new_sent_list.append(para_list[0])
            new_chapter_list.append(chapter_id)
            sl_chpt_num_list.append("0")
            if para_list[1].startswith('by') or para_list[1].startswith('By') or para_list[1].startswith('Written'):
                m_date = re.search(r"^.*(\d+).*$",para_list[1])
                if m_date:
                    new_sent_list.append(para_list[1])
                else:
                    new_sent_list.append(para_list[1])
                    new_chapter_list.append(chapter_id)
            else:
                #将默认循环起始值调整为第二行
                i = 1
            for j, para in enumerate(para_list[i:], start = i):
                m,sent_end = self._chapter_detector(para, sent_end)
                if m == 'on':
                    if para == para_list[2]:
                        m = re.search(r'^To|^For', para)
                        if m:
                            new_sent_list.append(para)
                            new_chapter_list.append(chapter_id)
                        else:
                            chapter_id = para
                            sl_chpt_num_list.append(str(j))
                            new_sent_list.append(para)
                            new_chapter_list.append(chapter_id)
                    else:
                        sl_chpt_num_list.append(str(j))
                        chapter_id = para
                        new_sent_list.append(para)
                        new_chapter_list.append(chapter_id)
                else:
                    new_sent_list.append(para)
                    new_chapter_list.append(chapter_id)
                
        #print('chapter added and out')
              
        return new_sent_list, new_chapter_list, sl_chpt_num_list

        #auto_filler_group
    def swap_chapter(self, tl_num_sent_list, sl_chapt_num_list):
        #print("start swap chapter")
        #必须核实num类型是否为数字类型。
        chapter_list = []
        for num,sent in tl_num_sent_list:
            if isinstance(num,str):
                num = eval(num)
            else:
                pass
            if str(num-1) in sl_chapt_num_list:
                chapter_list.append('[T]' + sent)
            else:
                chapter_list.append(sent)
        temp_id = ''
        new_list = []
        for para in chapter_list:
            if para.startswith(r'[T]'):
                if para == chapter_list[0]:
                    #去除标题行有可能存在的副标题
                    para = para.split(r'（')[0].strip()
                    para = para.split(r'——')[0].strip()
                else:
                    para = para.strip()
                temp_id = para.replace('[T]', '')
                new_list.append((para.replace('[T]', ''), temp_id))
            else:
                new_list.append((para.replace('[T]', ''), temp_id))
        return new_list
