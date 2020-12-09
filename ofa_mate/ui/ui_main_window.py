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

import os

from PyQt5.QtCore import Qt,QSize,pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow,QGridLayout,QHBoxLayout,QVBoxLayout,QAction,QComboBox,QDoubleSpinBox,
                             QToolBox,QGroupBox,QPushButton,QLineEdit,QLabel,QRadioButton,QStatusBar,QButtonGroup,
                             QCheckBox,QCompleter,QAbstractItemView,QWidget,QListWidget,QTextEdit,QFileDialog)

class UIMainWindow(QMainWindow):
    open_file = pyqtSignal()
    reload_file = pyqtSignal()
    json_sl_filler = pyqtSignal()
    json_tl_filler = pyqtSignal()
    json_sl_refiller = pyqtSignal()
    json_tl_refiller = pyqtSignal()
    load_next_version = pyqtSignal()
    write_to_json = pyqtSignal()    

    def __init__(self,parent = None):
        super(UIMainWindow,self).__init__(parent)
       
        self._prompt_frame = QGroupBox('操作提示')
        self._prompt_frame.setAlignment(Qt.AlignCenter)        

        self.initial_prompt = "本工具将已清洁好的句对齐或段对齐语料自动转换成可与OFA ParaConc相兼容的数据文件，请按指示操作。\n步骤1：点击“打开单文件”，加载您要转换的某个原、译文在一起的单语料文件。\n       如果原、译文分文件保存，请先选择“多文件”，再点击“打开多文件”"
        self._prompt_2 = "您指定的双语语料已成功加载！\n步骤2：请核实系统为您自动填充的书名、作者、译者等元信息是否准确，如有误，请手动修改。\n       确认无误后，请点击源语语料下的“提交”按钮。"
        self._prompt_3 = "源语语料提交成功，正文预览窗口内展示的是待生成语料的标准三列格式。\n步骤3：请点击目标语料下的“提交”按钮，或点击“重填”按钮取消当前已提交的语料。"
        self._prompt_5 = "恭喜您，数据转码已完成，生成的json文件已为您存储在savedfiles文件夹内，将其直接放入OFA ParaConc之下的corpus目录中，再运行OFA ParaConc，即可对其进行检索。"

        self._prompt_frame_layout = QHBoxLayout()
        self._promptBox = QLabel()
        self._promptBox.setText(self.initial_prompt)
        self._promptBox.setFixedHeight(50)
        self._promptBox.setWordWrap(True)        
        self._prompt_frame_layout.addWidget(self._promptBox)
        self._prompt_frame.setLayout(self._prompt_frame_layout)

        self._fileloader_frame = QGroupBox('加载语料')
        self._fileloader_frame.setAlignment(Qt.AlignCenter)
        
        self._fileloader_src_layout = QHBoxLayout()
        self._file_openBox = QLineEdit()
        self._file_openBox.setFixedWidth(500)
        self._file_openBox.setReadOnly(True)
        self._file_openButton = QPushButton()
        self._file_openButton.setText('打开单文件')
        self._file_openButton.setFixedWidth(80)
        self._file_openButton.clicked[bool].connect(self.open_file)
        self._file_reloadButton = QPushButton('重新加载')
        self._file_reloadButton.setFixedWidth(80)
        self._file_reloadButton.clicked[bool].connect(self.reload_file)
        self._fileloader_src_layout.addWidget(self._file_openBox)
        self._fileloader_src_layout.addWidget(self._file_openButton)
        self._fileloader_src_layout.addWidget(self._file_reloadButton)

        self._fileloader_opt_layout = QGridLayout()     
        self._file_type_label = QLabel('文件类型：')
        self._file_type_label.setFixedWidth(60)
        self._file_type_box = QComboBox()
        self._file_type_box.setFixedWidth(100)
        self._file_type_box.addItem('txt')
        self._file_type_box.addItem('docx')
        self._file_type_box.addItem('xlsx')

        self._file_bind_label = QLabel('组合方式：')
        
        self._file_bind_label.setFixedWidth(60)
        self._file_bind_box = QComboBox()
        self._file_bind_box.setFixedWidth(100)
        self._file_bind_box.addItem('单文件')
        self._file_bind_box.addItem('多文件')
        self._file_num_label = QLabel('文件个数：')
        self._file_num_label.setFixedWidth(60)
        self._file_num_box = QDoubleSpinBox()
        self._file_num_box.setFixedWidth(60)
        self._file_num_box.setMinimum(1)
        self._file_num_box.setDecimals(0)
        self._file_num_box.setDisabled(True)
        self._file_portion_label = QLabel('双语比例：')
        self._file_portion_label.setFixedWidth(60)
        self._file_portion_label.setStatusTip('源语与目标语之间的比值，1英一中为1:1，1英2中为1：2，以此类推')
        self._file_portion_box = QDoubleSpinBox()
        self._file_portion_box.setDisabled(True)
        self._file_portion_box.setFixedWidth(60)
        self._file_portion_box.setMinimum(0)
        self._file_portion_box.setDecimals(0)
        self._file_portion_box.setPrefix("1:")
        self._file_portion_box.setValue(1)
        self._file_pos_label = QLabel('双语位置：')
        self._file_pos_label.setFixedWidth(60)
        self._file_pos_box = QComboBox()
        self._file_pos_box.setDisabled(True)
        self._file_pos_box.setFixedWidth(100)
        
        self._file_pos_box.addItem('英上中下')
        self._file_pos_box.addItem('中上英下')
        self._file_pos_box.addItem('英左中右')
        self._file_pos_box.addItem('中左英右')
        self._file_pos_box.addItem('双语分离')

        self._fileloader_mark_layout = QGridLayout()
        self._fileloader_mark_label = QLabel('检索标记：')
        self._fileloader_mark_label.setFixedWidth(60)
        self._file_num_mark_box = QCheckBox('统一行号')
        self._file_num_mark_box.setFixedWidth(80)
        self._file_num_mark_box.setStatusTip('位于句或段之前，用“tab标记”分隔的或处于不同表格中的的统一行号')
        self._file_num_mark_box.clicked[bool].connect(self.mark_num)
        self._file_num_mark_box.setDisabled(True)
        self._file_chapt_num_box = QCheckBox('篇章标题')
        self._file_chapt_num_box.setFixedWidth(80)
        self._file_chapt_num_box.setStatusTip('句或段+“tab标记”+章节标题或全篇标题格式')
        self._file_chapt_num_box.clicked[bool].connect(self.mark_chapter)
        self._file_chapt_num_box.setDisabled(True)
        self._file_tab_mark_box = QCheckBox('“tab”标记')        
        self._file_tab_mark_box.setFixedWidth(100)
        self._file_tab_mark_box.setStatusTip('将行号和/或双语用“tab标记”进行分隔的双语左右对齐文件')
        self._file_tab_mark_box.clicked[bool].connect(self.mark_tab)
        self._file_tab_mark_box.setDisabled(True)
        self._file_cuc_mark_box = QCheckBox('“<seg>”标记')
        self._file_cuc_mark_box.setFixedWidth(100)
        self._file_cuc_mark_box.setStatusTip('格式为 <seg id = "...">正文</seg> 的ParaConc双语上下对齐文件')
        self._file_cuc_mark_box.clicked[bool].connect(self.mark_cuc)
        self._file_cuc_mark_box.setDisabled(True)
        self._file_table_mark_box = QCheckBox('表格标记')        
        self._file_table_mark_box.setFixedWidth(100)
        self._file_table_mark_box.setStatusTip('用于包含文本的表格，如WORD中的表格或EXCEL中的单元格')
        self._file_table_mark_box.clicked[bool].connect(self.mark_table)
        self._file_table_mark_box.setDisabled(True)
        self._fileloader_mark_layout.addWidget(self._fileloader_mark_label,0,0)
        self._fileloader_mark_layout.addWidget(self._file_num_mark_box,0,1)
        self._fileloader_mark_layout.addWidget(self._file_chapt_num_box,0,2)
        self._fileloader_mark_layout.addWidget(self._file_tab_mark_box,0,3)
        self._fileloader_mark_layout.addWidget(self._file_cuc_mark_box,0,4)
        self._fileloader_mark_layout.addWidget(self._file_table_mark_box,0,5) 
        
        self._fileloader_opt_layout.addWidget(self._file_type_label,0,0)
        self._fileloader_opt_layout.addWidget(self._file_type_box,0,1)
        self._fileloader_opt_layout.addWidget(self._file_bind_label,0,2)
        self._fileloader_opt_layout.addWidget(self._file_bind_box,0,3)
        self._fileloader_opt_layout.addWidget(self._file_pos_label,0,4)
        self._fileloader_opt_layout.addWidget(self._file_pos_box,0,5)
        self._fileloader_opt_layout.addWidget(self._file_num_label,0,6)
        self._fileloader_opt_layout.addWidget(self._file_num_box,0,7)        
        self._fileloader_opt_layout.addLayout(self._fileloader_mark_layout,1,0,1,6)
        self._fileloader_opt_layout.addWidget(self._file_portion_label,1,6)
        self._fileloader_opt_layout.addWidget(self._file_portion_box,1,7)

        self._fileloader_frame_layout = QVBoxLayout()
        self._fileloader_frame_layout.addLayout(self._fileloader_opt_layout)
        self._fileloader_frame_layout.addLayout(self._fileloader_mark_layout)
        self._fileloader_frame_layout.addLayout(self._fileloader_src_layout)
        self._fileloader_frame_layout.setAlignment(Qt.AlignCenter)
        
        self._fileloader_frame.setLayout(self._fileloader_frame_layout)
        self._fileloader_frame_layout.setAlignment(Qt.AlignCenter)
      
        self._generator_frame = QGroupBox('语料概况')
        self._generator_frame.setAlignment(Qt.AlignCenter)

        self._ss_book_frame = QGroupBox('源语语料')
        self._ss_book_frame.setAlignment(Qt.AlignCenter)
       
        self._ss_book_frame_layout = QGridLayout()
        self._ss_book_title = QLabel('书名：')
        self._ss_book_title.setFixedWidth(30)
        self._ss_book_title.setStatusTip('当前语料名称或所属合集名称')
        self._ss_book_titleBox = QLineEdit()
        self._ss_book_version = QLabel('版本：')
        self._ss_book_version.setFixedWidth(30)
        self._ss_book_versionBox = QLineEdit()
        self._ss_book_versionBox.setFixedWidth(120)
        self._ss_book_versionBox.setText('s0')
        self._ss_book_versionBox.setReadOnly(True)
        self._ss_book_versionBox.setEnabled(False)
        self._ss_book_language = QLabel('语言：')
        self._ss_book_language.setFixedWidth(30)
        self._ss_book_languageBox = QLineEdit()
        self._ss_book_languageBox.setFixedWidth(120)
        self._ss_book_languageBox.setText('en')
        self._ss_book_author = QLabel('作者：')
        self._ss_book_author.setFixedWidth(30)
        self._ss_book_author.setStatusTip('填写作者的标准的源语姓名')
        self._ss_book_authorBox = QLineEdit()
        self._ss_book_authorBox.setFixedWidth(120)
        self._ss_book_translator = QLabel('译者：')
        self._ss_book_translator.setFixedWidth(30)
        self._ss_book_translatorBox = QLineEdit()
        self._ss_book_translatorBox.setFixedWidth(120)
        self._ss_book_translatorBox.setEnabled(False)
        self._ss_book_date = QLabel('年代：')
        self._ss_book_date.setFixedWidth(30)
        self._ss_book_date.setStatusTip('填写源语作品发行年代，如1971；不详则留空')
        self._ss_book_dateBox = QLineEdit()
        self._ss_book_dateBox.setFixedWidth(120)
        self._ss_book_genre = QLabel('体裁：')
        self._ss_book_genre.setFixedWidth(30)
        self._ss_book_genre.setStatusTip('填写作品文体类型，如novel等')
        self._ss_book_genreBox = QLineEdit()
        self._ss_book_genreBox.setFixedWidth(120)
        self._ss_book_contents = QLabel('正文预览：')
        self._ss_book_contents.setFixedWidth(60)
        self._ss_book_contentsBox = QTextEdit()
        self._ss_book_contentsBox.setReadOnly(True)
        
        self._ss_book_buttonLayout = QHBoxLayout()
        self._ss_book_redoButton = QPushButton("重填")
        self._ss_book_redoButton.setFixedWidth(80)
        self._ss_book_redoButton.setEnabled(False)
        self._ss_book_redoButton.clicked[bool].connect(self.json_sl_refiller)
        self._ss_book_uploadButton = QPushButton("提交")
        self._ss_book_uploadButton.setFixedWidth(80)
        self._ss_book_uploadButton.clicked[bool].connect(self.json_sl_filler)
        self._ss_book_buttonLayout.addWidget(self._ss_book_redoButton)
        self._ss_book_buttonLayout.addWidget(self._ss_book_uploadButton)

        self._ss_book_frame_layout.addWidget(self._ss_book_title,0,0)
        self._ss_book_frame_layout.addWidget(self._ss_book_titleBox,0,1,1,3)
        self._ss_book_frame_layout.addWidget(self._ss_book_version,1,0)
        self._ss_book_frame_layout.addWidget(self._ss_book_versionBox,1,1)
        self._ss_book_frame_layout.addWidget(self._ss_book_language,1,2)
        self._ss_book_frame_layout.addWidget(self._ss_book_languageBox,1,3)
        self._ss_book_frame_layout.addWidget(self._ss_book_author,2,0)
        self._ss_book_frame_layout.addWidget(self._ss_book_authorBox,2,1)
        self._ss_book_frame_layout.addWidget(self._ss_book_translator,2,2)
        self._ss_book_frame_layout.addWidget(self._ss_book_translatorBox,2,3)
        self._ss_book_frame_layout.addWidget(self._ss_book_date,3,0)
        self._ss_book_frame_layout.addWidget(self._ss_book_dateBox,3,1)
        self._ss_book_frame_layout.addWidget(self._ss_book_genre,3,2)
        self._ss_book_frame_layout.addWidget(self._ss_book_genreBox,3,3)
        self._ss_book_frame_layout.addWidget(self._ss_book_contents,4,0,1,2)
        self._ss_book_frame_layout.addWidget(self._ss_book_contentsBox,5,0,8,4)
        self._ss_book_frame_layout.addLayout(self._ss_book_buttonLayout,15,0,1,4)
        self._ss_book_frame.setLayout(self._ss_book_frame_layout)
        
        self._tt_book_frame = QGroupBox('目标语语料')
        self._tt_book_frame.setAlignment(Qt.AlignCenter)       
       
        self._tt_book_frame_layout = QGridLayout()
        self._tt_book_title = QLabel('书名：')
        self._tt_book_title.setFixedWidth(30)
        self._tt_book_title.setStatusTip('当前语料名称或所属合集名称的译名')
        self._tt_book_titleBox = QLineEdit()
        self._tt_book_version = QLabel('版本：')
        self._tt_book_version.setFixedWidth(30)
        self._tt_book_version.setStatusTip('填写译本的阿拉伯数字编号，以t为首字母，如t1')
        self._tt_book_versionBox = QLineEdit()
        self._tt_book_versionBox.setFixedWidth(120)
        self._tt_book_versionBox.setText('t1')
        self._tt_book_language = QLabel('语言：')
        self._tt_book_language.setFixedWidth(30)
        self._tt_book_languageBox = QLineEdit()
        self._tt_book_languageBox.setFixedWidth(120)
        self._tt_book_languageBox.setText('zh')
        self._tt_book_author = QLabel('作者：')
        self._tt_book_author.setFixedWidth(30)
        self._tt_book_author.setStatusTip('填写源语作者的标准的中文译名')
        self._tt_book_authorBox = QLineEdit()
        self._tt_book_authorBox.setFixedWidth(120)
        self._tt_book_translator = QLabel('译者：')
        self._tt_book_translator.setFixedWidth(30)
        self._tt_book_translator.setStatusTip('填写译者姓名，若为多人，用“;”号分隔')
        self._tt_book_translatorBox = QLineEdit()
        self._tt_book_translatorBox.setFixedWidth(120)
        self._tt_book_date = QLabel('年代：')
        self._tt_book_date.setFixedWidth(30)
        self._tt_book_date.setStatusTip('填写译作发行年代，如1971；不详则留空')
        self._tt_book_dateBox = QLineEdit()
        self._tt_book_dateBox.setFixedWidth(120)
        self._tt_book_genre = QLabel('体裁：')
        self._tt_book_genre.setFixedWidth(30)
        self._tt_book_genre.setStatusTip('填写作品文体类型，如长篇小说等')
        self._tt_book_genreBox = QLineEdit()
        self._tt_book_genreBox.setFixedWidth(120)
        self._tt_book_contents = QLabel('正文预览：')
        self._tt_book_contents.setFixedWidth(60)
        self._tt_book_contentsBox = QTextEdit()
        self._tt_book_contentsBox.setReadOnly(True)

        self._tt_book_buttonLayout = QHBoxLayout()
        self._tt_book_redoButton = QPushButton("重填")
        self._tt_book_redoButton.setEnabled(False)
        self._tt_book_redoButton.setFixedWidth(80)
        self._tt_book_redoButton.clicked[bool].connect(self.json_tl_refiller)
        self._tt_book_uploadButton = QPushButton("提交")
        self._tt_book_uploadButton.setFixedWidth(80)
        self._tt_book_uploadButton.clicked[bool].connect(self.json_tl_filler)
        self._tt_book_uploadButton.setEnabled(False)
        self._tt_book_nextButton = QPushButton("下一译本")
        self._tt_book_nextButton.setFixedWidth(80)
        self._tt_book_nextButton.setEnabled(False)
        self._tt_book_nextButton.clicked[bool].connect(self.load_next_version)
        self._tt_book_buttonLayout.addWidget(self._tt_book_redoButton)
        self._tt_book_buttonLayout.addWidget(self._tt_book_nextButton)
        self._tt_book_buttonLayout.addWidget(self._tt_book_uploadButton)
        
        self._tt_book_frame_layout.addWidget(self._tt_book_title,0,0)
        self._tt_book_frame_layout.addWidget(self._tt_book_titleBox,0,1,1,3)
        self._tt_book_frame_layout.addWidget(self._tt_book_version,1,0)
        self._tt_book_frame_layout.addWidget(self._tt_book_versionBox,1,1)
        self._tt_book_frame_layout.addWidget(self._tt_book_language,1,2)
        self._tt_book_frame_layout.addWidget(self._tt_book_languageBox,1,3)
        self._tt_book_frame_layout.addWidget(self._tt_book_author,2,0)
        self._tt_book_frame_layout.addWidget(self._tt_book_authorBox,2,1)
        self._tt_book_frame_layout.addWidget(self._tt_book_translator,2,2)
        self._tt_book_frame_layout.addWidget(self._tt_book_translatorBox,2,3)
        self._tt_book_frame_layout.addWidget(self._tt_book_date,3,0)
        self._tt_book_frame_layout.addWidget(self._tt_book_dateBox,3,1)
        self._tt_book_frame_layout.addWidget(self._tt_book_genre,3,2)
        self._tt_book_frame_layout.addWidget(self._tt_book_genreBox,3,3)
        self._tt_book_frame_layout.addWidget(self._tt_book_contents,4,0,1,2)
        self._tt_book_frame_layout.addWidget(self._tt_book_contentsBox,5,0,8,4)
        self._tt_book_frame_layout.addLayout(self._tt_book_buttonLayout,15,0,1,4)
        self._tt_book_frame.setLayout(self._tt_book_frame_layout)
        
        self._generator_frame_layout = QHBoxLayout()
        self._generator_frame_layout.addWidget(self._ss_book_frame)
        self._generator_frame_layout.addWidget(self._tt_book_frame)
        self._generator_frame.setLayout(self._generator_frame_layout)


        self._convert_layout = QHBoxLayout()
        self._bi_book_convertButton = QPushButton("转换格式")
        self._bi_book_convertButton.clicked[bool].connect(self.write_to_json)
        self._bi_book_convertButton.setFixedWidth(80)
        self._bi_book_convertButton.setStyleSheet("font:bold")
        self._convert_layout.addWidget(self._bi_book_convertButton)
        self._convert_layout.setAlignment(Qt.AlignRight)
        
        mainWidget = QWidget()
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setSpacing(2)
        mainLayout.addWidget(self._prompt_frame,1)
        mainLayout.addWidget(self._fileloader_frame,1)
        mainLayout.addWidget(self._generator_frame,8)
        mainLayout.addLayout(self._convert_layout,1)
        self.setCentralWidget(mainWidget)
        

        #----------创建主窗口状态栏----------
        self._statusBar = QStatusBar()        
        self._statusBar.showMessage('欢迎使用 OFA Mate')
        self._copyRightLabel = QLabel("Copyright © 2020 Tony Chang @ English Cafeteria")
        self._statusBar.addPermanentWidget(self._copyRightLabel)
        self.setStatusBar(self._statusBar)
        
        
        #----------设置页面尺寸及标题等----------
        self.setGeometry(200, 50, 600, 600)    
        self.setObjectName("MainWindow")
        currentDir = os.getcwd()
        self.setWindowTitle("傲飞伴侣：一对多平行语料格式转换工具")
        self.setWindowIcon(QIcon(currentDir +"/app_data/workfiles/myIcon.png"))
        self.setIconSize(QSize(100, 40))

        self._file_type_box.activated[str].connect(self._type_index_info)
        self._file_bind_box.activated[str].connect(self._bind_index_info)
        self._file_pos_box.activated[str].connect(self._pos_index_info)
        self._file_type_box.currentIndexChanged.connect(self._type_index_sender)        
        self._file_bind_box.currentIndexChanged.connect(self._bind_index_sender)        
        self._file_pos_box.currentIndexChanged.connect(self._pos_index_sender)

    # hardware_group
    def mark_num(self):
        if self._file_num_mark_box.isChecked():
            self._file_tab_mark_box.setChecked(True)
            self._file_cuc_mark_box.setChecked(False) 
        else:pass
        
    # hardware_group        
    def mark_chapter(self):
        if self._file_chapt_num_box.isChecked():
            pass
        else:pass
        
    # hardware_group
    def mark_tab(self):
        if self._file_tab_mark_box.isChecked():
            self._file_cuc_mark_box.setChecked(False)
            self._file_table_mark_box.setChecked(False)
            if self._file_type_box.currentIndex() != 0:
                self._file_type_box.setCurrentIndex(0)
            else:pass                
        elif self._file_tab_mark_box.isChecked() == False:
            self._file_num_mark_box.setChecked(False)
            self._file_chapt_num_box.setChecked(False)
        else:pass
        
    #hardware_group
    def mark_cuc(self):
        if self._file_cuc_mark_box.isChecked():
            self._file_num_mark_box.setChecked(True)
            self._file_chapt_num_box.setChecked(False)          
            self._file_tab_mark_box.setChecked(False)
            self._file_table_mark_box.setChecked(False)
            self._file_type_box.setCurrentIndex(0)
            if self._file_pos_box.currentIndex() in [0,1,4]:
                pass
            else:
                self._file_pos_box.setCurrentIndex(0)
        else:
            pass
        
    #hardware_group
    def mark_table(self):
        if self._file_table_mark_box.isChecked():
            self._file_cuc_mark_box.setChecked(False)
            self._file_tab_mark_box.setChecked(False)
            if self._file_type_box.currentIndex() != 0:
                pass
            else:
                self._file_type_box.setCurrentIndex(2)
        elif self._file_table_mark_box.isChecked() == False:
            if self._file_type_box.currentIndex() == 0:
                pass
            else:
                self._file_type_box.setCurrentIndex(0)
        else:pass
        
    #hardware_group
    def _bind_index_info(self,text):
        if text == "单文件":
            if self._file_portion_box.value() == 1:
                pass
            else:
                self._file_portion_box.setValue(1)
            self._file_num_box.setEnabled(True)
            self._file_num_box.setMinimum(1)
            self._file_num_box.setValue(1)
            self._file_num_box.setEnabled(False)
            self._file_pos_box.setCurrentIndex(0)
            if self._file_openButton.text() == "打开单文件":
                pass
            else:
                self._file_openButton.setText('打开单文件')
        if text == "多文件":
            self._file_portion_box.setValue(0)
            self._file_num_box.setEnabled(True)
            self._file_num_box.setMinimum(2)
            self._file_pos_box.setCurrentIndex(4)
            self._file_portion_box.setValue(0)
            if self._file_openButton.text() == "打开多文件":
                pass
            else:
                self._file_openButton.setText('打开多文件')
        else:pass
        
    #hardware_group    
    def _bind_index_sender(self,i):
        if self._file_bind_box.currentText() == "单文件":
            #self._file_portion_box.setValue(1)
            if self._file_openButton.text() == "打开单文件":
                pass
            else:
                self._file_openButton.setText('打开单文件')
        elif self._file_bind_box.currentText() == "多文件":
            #self._file_portion_box.setValue(0)
            if self._file_openButton.text() == "打开多文件":
                pass
            else:
                self._file_openButton.setText('打开多文件')
        else:pass
        
    #hardware_group
    def _pos_index_info(self,text):
        if text == "双语分离":
            self._file_portion_box.setValue(0)
            if self._file_bind_box.currentText()  != '多文件':
                self._file_bind_box.setCurrentIndex(1)
                self._file_num_box.setEnabled(True)
                self._file_num_box.setMinimum(2)
            else:pass
        else:
            self._file_portion_box.setValue(1)
            if text in ["英上中下","中上英下"]:
                self._file_bind_box.setCurrentIndex(0)
                self._file_num_box.setEnabled(False)
            elif text in ["英左中右","中左英右"]:
                self._file_bind_box.setCurrentIndex(0)
                self._file_num_box.setEnabled(False)
                self._file_cuc_mark_box.setChecked(False)
                if self._file_type_box.currentIndex() == 0:
                    self._file_tab_mark_box.setChecked(True)
                else:pass                
            else:pass
    #hardware_group    
    def _pos_index_sender(self,text):
        if text in ["英上中下","中上英下"]:
            self._file_bind_box.setCurrentIndex(0)
            self._file_num_box.setEnabled(False)
        elif text in ["英左中右","中左英右"]:
            self._file_bind_box.setCurrentIndex(0)
            self._file_num_box.setEnabled(False)
            self._file_tab_mark_box.setChecked(True)
            self._file_cuc_mark_box.setChecked(False)
        elif text == "双语分离":
            #self._file_portion_box.setValue(0)
            if self._file_bind_box.currentText()  != '多文件':
                self._file_bind_box.setCurrentIndex(1)
                self._file_num_box.setEnabled(True)
                self._file_num_box.setMinimum(2)
            else:pass
        else:
            pass
    #hardware_group    
    def _type_index_info(self,text):
        file_suffix = text
        if file_suffix == "xlsx":
            self._file_num_mark_box.setChecked(True)
            self._file_pos_box.setCurrentIndex(2)
            self._file_table_mark_box.setChecked(True)
            self._file_tab_mark_box.setChecked(True)
        elif file_suffix == 'txt':
            self._file_table_mark_box.setChecked(False)
        elif file_suffix == 'docx':
            self._file_pos_box.setCurrentIndex(0)
            self._file_tab_mark_box.setChecked(False)
            self._file_cuc_mark_box.setChecked(False)
        else:pass
    
    #hardware_group    
    def _type_index_sender(self,i):
        file_suffix = self._file_type_box.currentText()
        if file_suffix == "xlsx":
            self._file_table_mark_box.setChecked(True)
        else:pass
    
    #prompt_group
    def _set_status_text(self,text):
        self._statusBar.showMessage(text,10000)

