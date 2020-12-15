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

import os, re

class InfoCollector:

    def __init__(self):
        self.title = ""
        self.author = ""
        self.translator = ""
        self.date = ""
        
    def info_collector_en(self, sl,tl,para_list = []):
        if para_list == []:
            self.title = ""
            self.author = ""
            self.translator = ""
            self.date = ""
        else:
            if "\t" in para_list[0]:
                para_sents = para_list[0].split('\t')
                for item in para_sents:
                    if item.isnuemric() == False:
                        para_sent_1 = item
                        break
            else:
                para_sent_1 = para_list[0]

            if "\t" in para_list[1]:
                para_sents = para_list[1].split('\t')
                for item in para_sents:
                    if item.isnuemric() == False:
                        para_sent_2 = item
                        break
            else:
                para_sent_2 = para_list[1]

            title = para_sent_1.split('--')[0].strip()
            if title.isupper():
                self.title = title.title()
            else:
                self.title = title
            if para_sent_2:
                m_date = re.search(r"^.*(\d{4}).*$", para_sent_2)
                if m_date:
                    self.date = m_date.group(1)
                else:
                    self.date = ""
                m_author_translator = re.search(r"by\s+[A-Z].*(translated by|Translated by|tr.|Tr.)\s+([A-Z].*)", para_sent_2)
                m_translator = re.search(r"(translated by|Translated by|tr.|Tr.)\s+([A-Z].*)", para_sent_2)
                m_author = re.search(r"((by|By|BY)\s+[A-Z].*\,)|((by|By|BY)\s+[A-Z].*)", para_sent_2)
                if m_author_translator:
                    m_author_translator_text = m_author_translator.group()
                    author = re.sub(r'(translated by|Translated by|tr.|Tr.)\s+([A-Z].*)','', m_author_translator_text)
                    author = re.sub(r'(By|by)\s+','',author)
                    self.author = re.sub(r'(\,|\;)','',author)
                    self.translator = re.split("(translated by|Translated by|tr.|Tr.)\s+",m_author_translator_text)[-1]
                    self.translator = self.translator.split(',')[0]
                elif m_translator:
                    translator = m_translator.group()
                    translator = re.sub(r"(translated by|Translated by|tr.|Tr.)\s+", "",translator)
                    if translator.isupper():
                        self.translator = translator.title()
                    else:
                        self.translator = translator
                    self.author = ""
                else:
                    self.translator = ''
                    self.author = ""
                if self.author and self.translator:
                    pass
                elif self.translator:
                    if m_author:
                        author = m_author.group()
                        author = re.sub(r"(by|By|BY)\s+", "", author)
                        author = author.replace(",",'')
                        if author.isupper():
                            self.author = author.title()
                        else:
                            self.author = author
                else:
                    if m_author:
                        author = m_author.group()
                        author = re.sub(r"(by|By|BY)\s+", "", author)
                        author = author.replace(",",'')
                        if author.isupper():
                            self.author = author.title()
                        else:
                            self.author = author
                        self.translator = ""
                        if tl == 'en':
                            self.translator = self.author
                            self.author = ""
                    else:
                        self.translator = ""
                        self.author = ""
            else:
                self.date = ""
                self.author = ""
                self.translator = ""
        return self.title, self.author, self.translator, self.date

    def info_collector_zh(self, para_list = []):
        if para_list == []:
            self.title = ""
            self.author = ""
            self.translator = ""
            self.date = ""
        else:
            # To Do: 摘译本第一行基本无数据，需要特别判断一下
            if "\t" in para_list[0]:
                para_sents = para_list[0].split('\t')
                for item in para_sents:
                    if item.isnuemric() == False:
                        para_sent_1 = item
                        break
            else:
                para_sent_1 = para_list[0]

            self.title = para_sent_1.split('（')[0].split('—')[0]
            #self.title = self.title.replace("《","").repalce("》","")

            if "\t" in para_list[1]:
                para_sents = para_list[1].split('\t')
                for item in para_sents:
                    if item.isnuemric() == False:
                        para_sent_2 = item
                        break
            else:
                para_sent_2 = para_list[1]

            m_date = re.finditer(r"\d{4}",para_sent_2)
            if m_date:
                try:
                    m_date_list = [m.group() for m in m_date]
                    if len(m_date_list) == 1:
                        self.date = m_date_list[0]
                    elif len(m_date_list) >= 2:
                        self.date = m_date_list[-1]
                    else:
                        self.date = m_date_list[0]
                except:
                    #print("date error!")
                    self.date = ""
                    pass
            else:
                self.date = ""
            # To Do: 存在“校对”，有必要在整体上补加相关空位
            m_author_zh = re.search(r"(.*)著", para_sent_2)
            m_translator_zh = re.search(r"(.*)译", para_sent_2)

            if m_author_zh:
                try:
                    author = m_author_zh.group().replace("著","")
                    author = author.strip()
                    if '[' in author:
                        self.author = '[' + author.split('[')[1]
                    elif '〔' in author:
                        self.author = '〔' + author.split('〔')[1]
                    elif '》' in author:
                        self.author = author.split('》')[1]
                    else:
                        self.author = author
                except:
                    self.author = ""
            if m_translator_zh:
                try:
                    translator = m_translator_zh.group().replace("译","")
                    translator = translator.strip()
                    if '[' in translator:
                        self.translator = '['+translator.split('[')[1]
                    elif '〔' in translator:
                        self.translator = '〔'+translator.split('〔')[1]
                    elif '》' in translator:
                        self.translator = translator.split('》')[1]
                    else:
                        self.translator = translator
                except:
                    self.translator = ""
                    pass
            else:
                self.translator = ""

        return self.title, self.author, self.translator, self.date

