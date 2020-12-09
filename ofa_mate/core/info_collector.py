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
        
    def info_collector_en(self, para_list = []):
        if para_list == []:
            self.title = ""
            self.author = ""
            self.translator = ""
            self.date = ""
        else:
            self.translator = ""
            title = para_list[0].split('--')[0].strip()
            if title.isupper():
                self.title = title.title()
            else:
                self.title = title
            if para_list[1]:            
                m_date = re.search(r"^.*(\d{4}).*$", para_list[1])
                if m_date:
                    self.date = m_date.group(1)
                else:
                    self.date = ""
                m_author = re.search(r"(by|By|BY)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)", para_list[1])
                if m_author:
                    author = m_author.group()
                    author = re.sub(r"(by|By|BY)\s+", "", author)
                    if author.isupper():
                        self.author = author.title()
                    else:
                        self.author = author
                else:
                    self.author = ""
            else:
                self.date = ""
                self.author = ""
        return self.title, self.author, self.translator, self.date

    def info_collector_zh(self,para_list = []):
        if para_list == []:
            self.title = ""
            self.author = ""
            self.translator = ""
            self.date = ""
        else:
            # To Do: 摘译本第一行基本无数据，需要特别判断一下
            self.title = para_list[0].split('（')[0].split('—')[0]
            m_date = re.finditer(r"\d{4}",para_list[1])
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
                    print("date error!")
                    self.date = ""
                    pass
            else:
                self.date = ""
            # To Do: 存在“校对”，有必要在整体上补加相关空位
            m_author_zh = re.search(r"(.*)著(.*)译", para_list[1])
            if m_author_zh:
                try:
                    author = m_author_zh.group(1).strip()
                    self.translator = m_author_zh.group(2).split('；')[-1].split(';')[-1].strip()
                    if '[' in author:
                        self.author = '['+author.split('[')[1]
                    elif '〔' in author:
                        self.author = '〔'+author.split('〔')[1]
                    elif '》' in author:
                        self.author = author.split('》')[1]
                    else:
                        self.author = author
                except:
                    self.author = ""
                    self.translator = ""
                    print("author and translator error!")
                    pass
            else:
                m_author_zh_2 = re.search(r"(.*)译", para_list[1])
                if m_author_zh_2:
                    self.author = ""
                    self.translator = m_author_zh_2.group(1).split('；')[-1].split(';')[-1].strip()
                else:
                    self.author = ""
                    self.translator = ""
            
        return self.title, self.author, self.translator, self.date

