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

import os,json

from PyQt5.QtCore import Qt,QSize,pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow,QGridLayout,QHBoxLayout,QVBoxLayout,QAction,QComboBox,QDoubleSpinBox,
                             QToolBox,QGroupBox,QPushButton,QLineEdit,QLabel,QRadioButton,QStatusBar,QButtonGroup,
                             QCheckBox,QCompleter,QAbstractItemView,QWidget,QListWidget,QTextEdit,QFileDialog)

class UIMainWindow(QMainWindow):
    '''UI Frame'''
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
        currentDir = os.getcwd()
        dataDir = os.path.join(currentDir, "app_data")
        workFileDir = os.path.join(dataDir, "workfiles")
        self._outPutDir = os.path.join(currentDir, "savedfiles")
        self._interface_lang_file = os.path.join(workFileDir,'interface_language_setting.txt')
        self._interface_lang_dict = os.path.join(workFileDir,'interface_language_dict.json')
        self.fc_lg, self.fc_dict = self.set_lang()
       
        self._prompt_frame = QGroupBox(self.fc_dict["frame_prompt"][self.fc_lg])
        self._prompt_frame.setAlignment(Qt.AlignCenter)        

        self.initial_prompt = self.fc_dict["pmt_1_start"][self.fc_lg] + "\n" + self.fc_dict["pmt_1_a"][self.fc_lg] +"\n" + self.fc_dict["pmt_1_b"][self.fc_lg]
        self._prompt_2 = self.fc_dict["pmt_2_start"][self.fc_lg] + "\n " +  self.fc_dict["pmt_2_a"][self.fc_lg] + "\n " +  self.fc_dict["pmt_2_b"][self.fc_lg]
        self._prompt_3 = self.fc_dict["pmt_3_start"][self.fc_lg] + "\n " + self.fc_dict["pmt_3_a"][self.fc_lg]
        self._prompt_5 = self.fc_dict["pmt_5"][self.fc_lg]

        self._prompt_frame_layout = QHBoxLayout()
        self._promptBox = QLabel()
        self._promptBox.setText(self.initial_prompt)
        self._promptBox.setFixedHeight(80)
        self._promptBox.setWordWrap(True)        
        self._prompt_frame_layout.addWidget(self._promptBox)
        self._prompt_frame.setLayout(self._prompt_frame_layout)

        self._fileloader_frame = QGroupBox(self.fc_dict["frame_load"][self.fc_lg])
        self._fileloader_frame.setAlignment(Qt.AlignCenter)
        
        self._fileloader_src_layout = QHBoxLayout()
        self._file_openBox = QLineEdit()
        self._file_openBox.setFixedWidth(500)
        self._file_openBox.setReadOnly(True)
        self._file_openButton = QPushButton()
        self._file_openButton.setText(self.fc_dict["open_s"][self.fc_lg])
        self._file_openButton.setFixedWidth(80)
        self._file_openButton.clicked[bool].connect(self.open_file)
        self._file_reloadButton = QPushButton(self.fc_dict["r_load"][self.fc_lg])
        self._file_reloadButton.setFixedWidth(80)
        self._file_reloadButton.clicked[bool].connect(self.reload_file)
        self._fileloader_src_layout.addWidget(self._file_openBox)
        self._fileloader_src_layout.addWidget(self._file_openButton)
        self._fileloader_src_layout.addWidget(self._file_reloadButton)

        self._fileloader_opt_layout = QGridLayout()     
        self._file_type_label = QLabel(self.fc_dict["f_type"][self.fc_lg])
        self._file_type_label.setFixedWidth(60)
        self._file_type_box = QComboBox()
        self._file_type_box.setFixedWidth(100)
        self._file_type_box.addItem('txt')
        self._file_type_box.addItem('docx')
        self._file_type_box.addItem('xlsx')

        self._file_bind_label = QLabel(self.fc_dict["bi_loc"][self.fc_lg])
        
        self._file_bind_label.setFixedWidth(80)
        self._file_bind_box = QComboBox()
        self._file_bind_box.setFixedWidth(120)
        self._file_bind_box.addItem(self.fc_dict["bind_sig"][self.fc_lg])
        self._file_bind_box.addItem(self.fc_dict["bind_mul"][self.fc_lg])
        self._file_num_label = QLabel(self.fc_dict["f_num"][self.fc_lg])
        self._file_num_label.setFixedWidth(80)
        self._file_num_box = QDoubleSpinBox()
        self._file_num_box.setFixedWidth(80)
        self._file_num_box.setMinimum(1)
        self._file_num_box.setDecimals(0)
        self._file_num_box.setDisabled(True)
        self._file_portion_label = QLabel(self.fc_dict["bi_rate"][self.fc_lg])
        self._file_portion_label.setFixedWidth(80)
        self._file_portion_label.setStatusTip(self.fc_dict["tip_portion"][self.fc_lg])
        self._file_portion_box = QDoubleSpinBox()
        self._file_portion_box.setDisabled(True)
        self._file_portion_box.setFixedWidth(80)
        self._file_portion_box.setMinimum(0)
        self._file_portion_box.setDecimals(0)
        self._file_portion_box.setPrefix("1:")
        self._file_portion_box.setValue(1)
        self._file_pos_label = QLabel(self.fc_dict["bi_pos"][self.fc_lg])
        self._file_pos_label.setFixedWidth(80)
        self._file_pos_box = QComboBox()
        self._file_pos_box.setDisabled(True)
        self._file_pos_box.setFixedWidth(120)
        
        self._file_pos_box.addItem(self.fc_dict["u_d"][self.fc_lg])
        self._file_pos_box.addItem(self.fc_dict["l_r"][self.fc_lg])
        self._file_pos_box.addItem(self.fc_dict["bi-sep"][self.fc_lg])

        self._fileloader_mark_layout = QGridLayout()
        self._fileloader_mark_label = QLabel(self.fc_dict["conc_mk"][self.fc_lg])
        self._fileloader_mark_label.setFixedWidth(80)
        self._file_num_mark_box = QCheckBox(self.fc_dict["l_num"][self.fc_lg])
        self._file_num_mark_box.setFixedWidth(80)
        self._file_num_mark_box.setStatusTip(self.fc_dict["tip_num"][self.fc_lg])
        self._file_num_mark_box.clicked[bool].connect(self.mark_num)
        self._file_num_mark_box.setDisabled(True)
        self._file_chapt_num_box = QCheckBox(self.fc_dict["title_ch"][self.fc_lg])
        self._file_chapt_num_box.setFixedWidth(100)
        self._file_chapt_num_box.setStatusTip(self.fc_dict["tip_format"][self.fc_lg])
        self._file_chapt_num_box.clicked[bool].connect(self.mark_chapter)
        self._file_chapt_num_box.setDisabled(True)
        self._file_tab_mark_box = QCheckBox(self.fc_dict["mk_tab"][self.fc_lg])
        self._file_tab_mark_box.setFixedWidth(100)
        self._file_tab_mark_box.setStatusTip(self.fc_dict["tip_tab"][self.fc_lg])
        self._file_tab_mark_box.clicked[bool].connect(self.mark_tab)
        self._file_tab_mark_box.setDisabled(True)
        self._file_cuc_mark_box = QCheckBox(self.fc_dict["mk_seg"][self.fc_lg])
        self._file_cuc_mark_box.setFixedWidth(100)
        self._file_cuc_mark_box.setStatusTip(self.fc_dict["tip_seg"][self.fc_lg])
        self._file_cuc_mark_box.clicked[bool].connect(self.mark_cuc)
        self._file_cuc_mark_box.setDisabled(True)
        self._file_table_mark_box = QCheckBox(self.fc_dict["mk_table"][self.fc_lg])
        self._file_table_mark_box.setFixedWidth(100)
        self._file_table_mark_box.setStatusTip(self.fc_dict["tip_table"][self.fc_lg])
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
      
        self._generator_frame = QGroupBox(self.fc_dict["frame_profile"][self.fc_lg])
        self._generator_frame.setAlignment(Qt.AlignCenter)

        self._ss_book_frame = QGroupBox(self.fc_dict["win_sl"][self.fc_lg])
        self._ss_book_frame.setAlignment(Qt.AlignCenter)
       
        self._ss_book_frame_layout = QGridLayout()
        self._ss_book_title = QLabel(self.fc_dict["title_book"][self.fc_lg])
        self._ss_book_title.setFixedWidth(80)
        self._ss_book_title.setStatusTip(self.fc_dict["tip_fill_title"][self.fc_lg])
        self._ss_book_titleBox = QLineEdit()
        self._ss_book_version = QLabel(self.fc_dict["vn_num"][self.fc_lg])
        self._ss_book_version.setFixedWidth(80)
        self._ss_book_versionBox = QLineEdit()
        self._ss_book_versionBox.setFixedWidth(120)
        self._ss_book_versionBox.setText('s0')
        self._ss_book_versionBox.setReadOnly(True)
        self._ss_book_versionBox.setEnabled(False)
        self._ss_book_language = QLabel(self.fc_dict["corp_lang"][self.fc_lg])
        self._ss_book_language.setFixedWidth(80)
        self._ss_book_languageBox = QLineEdit()
        self._ss_book_languageBox.setFixedWidth(120)
        self._ss_book_languageBox.setText('en')
        self._ss_book_author = QLabel(self.fc_dict["ar_id"][self.fc_lg])
        self._ss_book_author.setFixedWidth(80)
        self._ss_book_author.setStatusTip(self.fc_dict["tip_fill_author"][self.fc_lg])
        self._ss_book_authorBox = QLineEdit()
        self._ss_book_authorBox.setFixedWidth(120)
        self._ss_book_translator = QLabel(self.fc_dict["tr_id"][self.fc_lg])
        self._ss_book_translator.setFixedWidth(80)
        self._ss_book_translatorBox = QLineEdit()
        self._ss_book_translatorBox.setFixedWidth(120)
        self._ss_book_translatorBox.setEnabled(False)
        self._ss_book_date = QLabel(self.fc_dict["issue_date"][self.fc_lg])
        self._ss_book_date.setFixedWidth(80)
        self._ss_book_date.setStatusTip(self.fc_dict["tip_fill_date"][self.fc_lg])
        self._ss_book_dateBox = QLineEdit()
        self._ss_book_dateBox.setFixedWidth(120)
        self._ss_book_genre = QLabel(self.fc_dict["issue_genre"][self.fc_lg])
        self._ss_book_genre.setFixedWidth(80)
        self._ss_book_genre.setStatusTip(self.fc_dict["tip_fill_genre"][self.fc_lg])
        self._ss_book_genreBox = QLineEdit()
        self._ss_book_genreBox.setFixedWidth(120)
        self._ss_book_contents = QLabel(self.fc_dict["win_preview"][self.fc_lg])
        self._ss_book_contents.setFixedWidth(120)
        self._ss_book_contentsBox = QTextEdit()
        self._ss_book_contentsBox.setReadOnly(True)
        
        self._ss_book_buttonLayout = QHBoxLayout()
        self._ss_book_redoButton = QPushButton(self.fc_dict["btn_refill"][self.fc_lg])
        self._ss_book_redoButton.setFixedWidth(80)
        self._ss_book_redoButton.setEnabled(False)
        self._ss_book_redoButton.clicked[bool].connect(self.json_sl_refiller)
        self._ss_book_uploadButton = QPushButton(self.fc_dict["btn_submit"][self.fc_lg])
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
        
        self._tt_book_frame = QGroupBox(self.fc_dict["win_tl"][self.fc_lg])
        self._tt_book_frame.setAlignment(Qt.AlignCenter)       
       
        self._tt_book_frame_layout = QGridLayout()
        self._tt_book_title = QLabel(self.fc_dict["title_book"][self.fc_lg])
        self._tt_book_title.setFixedWidth(80)
        self._tt_book_title.setStatusTip(self.fc_dict["tip_fill_title_tl"][self.fc_lg])
        self._tt_book_titleBox = QLineEdit()
        self._tt_book_version = QLabel(self.fc_dict["vn_num"][self.fc_lg])
        self._tt_book_version.setFixedWidth(80)
        self._tt_book_version.setStatusTip(self.fc_dict["tip_fill_vn"][self.fc_lg])
        self._tt_book_versionBox = QLineEdit()
        self._tt_book_versionBox.setFixedWidth(120)
        self._tt_book_versionBox.setText('t1')
        self._tt_book_language = QLabel(self.fc_dict["corp_lang"][self.fc_lg])
        self._tt_book_language.setFixedWidth(80)
        self._tt_book_languageBox = QLineEdit()
        self._tt_book_languageBox.setFixedWidth(120)
        self._tt_book_languageBox.setText('zh')
        self._tt_book_author = QLabel(self.fc_dict["ar_id"][self.fc_lg])
        self._tt_book_author.setFixedWidth(80)
        self._tt_book_author.setStatusTip(self.fc_dict["tip_fill_author_tl"][self.fc_lg])
        self._tt_book_authorBox = QLineEdit()
        self._tt_book_authorBox.setFixedWidth(120)
        self._tt_book_translator = QLabel(self.fc_dict["tr_id"][self.fc_lg])
        self._tt_book_translator.setFixedWidth(80)
        self._tt_book_translator.setStatusTip(self.fc_dict["tip_fill_trans"][self.fc_lg])
        self._tt_book_translatorBox = QLineEdit()
        self._tt_book_translatorBox.setFixedWidth(120)
        self._tt_book_date = QLabel(self.fc_dict["issue_date"][self.fc_lg])
        self._tt_book_date.setFixedWidth(80)
        self._tt_book_date.setStatusTip(self.fc_dict["tip_fill_date_tl"][self.fc_lg])
        self._tt_book_dateBox = QLineEdit()
        self._tt_book_dateBox.setFixedWidth(120)
        self._tt_book_genre = QLabel(self.fc_dict["issue_genre"][self.fc_lg])
        self._tt_book_genre.setFixedWidth(80)
        self._tt_book_genre.setStatusTip(self.fc_dict["tip_fill_genre_tl"][self.fc_lg])
        self._tt_book_genreBox = QLineEdit()
        self._tt_book_genreBox.setFixedWidth(120)
        self._tt_book_contents = QLabel(self.fc_dict["win_preview"][self.fc_lg])
        self._tt_book_contents.setFixedWidth(120)
        self._tt_book_contentsBox = QTextEdit()
        self._tt_book_contentsBox.setReadOnly(True)

        self._tt_book_buttonLayout = QHBoxLayout()
        self._tt_book_redoButton = QPushButton(self.fc_dict["btn_refill"][self.fc_lg])
        self._tt_book_redoButton.setEnabled(False)
        self._tt_book_redoButton.setFixedWidth(80)
        self._tt_book_redoButton.clicked[bool].connect(self.json_tl_refiller)
        self._tt_book_uploadButton = QPushButton(self.fc_dict["btn_submit"][self.fc_lg])
        self._tt_book_uploadButton.setFixedWidth(80)
        self._tt_book_uploadButton.clicked[bool].connect(self.json_tl_filler)
        self._tt_book_uploadButton.setEnabled(False)
        self._tt_book_nextButton = QPushButton(self.fc_dict["btn_next"][self.fc_lg])
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
        self._bi_book_convertButton = QPushButton(self.fc_dict["btn_conv"][self.fc_lg])
        self._bi_book_convertButton.clicked[bool].connect(self.write_to_json)
        self._bi_book_convertButton.setFixedWidth(120)
        self._bi_book_convertButton.setStyleSheet("font:bold")
        self._convert_layout.addWidget(self._bi_book_convertButton)
        self._convert_layout.setAlignment(Qt.AlignCenter)
        
        mainWidget = QWidget()
        mainLayout = QVBoxLayout(mainWidget)
        mainLayout.setSpacing(2)
        mainLayout.addWidget(self._prompt_frame,0)
        mainLayout.addWidget(self._fileloader_frame,0)
        mainLayout.addWidget(self._generator_frame,9)
        mainLayout.addLayout(self._convert_layout,1)
        self.setCentralWidget(mainWidget)
        

        #----------创建主窗口状态栏----------
        self._statusBar = QStatusBar()        
        self._statusBar.showMessage(self.fc_dict["greeting"][self.fc_lg])
        self._copyRightLabel = QLabel(self.fc_dict["copyright"][self.fc_lg])
        self._statusBar.addPermanentWidget(self._copyRightLabel)
        self.setStatusBar(self._statusBar)
        
        
        #----------设置页面尺寸及标题等----------
        self.setGeometry(200, 50, 800, 600)
        self.setObjectName("MainWindow")
        currentDir = os.getcwd()
        self.setWindowTitle(self.fc_dict["soft_title"][self.fc_lg])
        self.setWindowIcon(QIcon(currentDir +"/app_data/workfiles/myIcon.png"))
        self.setIconSize(QSize(100, 40))

        self._file_type_box.activated[str].connect(self._type_index_info)
        self._file_bind_box.activated[str].connect(self._bind_index_info)
        self._file_pos_box.activated[str].connect(self._pos_index_info)
        self._file_type_box.currentIndexChanged.connect(self._type_index_sender)        
        self._file_bind_box.currentIndexChanged.connect(self._bind_index_sender)        
        self._file_pos_box.currentIndexChanged.connect(self._pos_index_sender)

    def set_lang(self):
        with open (self._interface_lang_file, mode = 'r', encoding = 'utf-8-sig') as f:
            default_lg = f.read().strip()
        with open (self._interface_lang_dict, mode = 'r', encoding = 'utf-8-sig') as f:
            lg_dict = json.loads(f.read())
        return default_lg, lg_dict
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
            if self._file_pos_box.currentIndex() in [0,2]:
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
        if text == self.fc_dict["bind_sig"][self.fc_lg]:
            if self._file_portion_box.value() == 1:
                pass
            else:
                self._file_portion_box.setValue(1)
            self._file_num_box.setEnabled(True)
            self._file_num_box.setMinimum(1)
            self._file_num_box.setValue(1)
            self._file_num_box.setEnabled(False)
            self._file_pos_box.setCurrentIndex(0)
            if self._file_openButton.text() == self.fc_dict["open_s"][self.fc_lg]:
                pass
            else:
                self._file_openButton.setText(self.fc_dict["open_s"][self.fc_lg])
        if text == self.fc_dict["bind_mul"][self.fc_lg]:
            self._file_portion_box.setValue(0)
            self._file_num_box.setEnabled(True)
            self._file_num_box.setMinimum(2)
            self._file_pos_box.setCurrentIndex(2)
            self._file_portion_box.setValue(0)
            if self._file_openButton.text() == self.fc_dict["open_m"][self.fc_lg]:
                pass
            else:
                self._file_openButton.setText(self.fc_dict["open_m"][self.fc_lg])
        else:pass
        
    #hardware_group    
    def _bind_index_sender(self,i):
        if self._file_bind_box.currentText() == self.fc_dict["bind_sig"][self.fc_lg]:
            #self._file_portion_box.setValue(1)
            if self._file_openButton.text() == self.fc_dict["open_s"][self.fc_lg]:
                pass
            else:
                self._file_openButton.setText(self.fc_dict["open_s"][self.fc_lg])
        elif self._file_bind_box.currentText() == self.fc_dict["bind_mul"][self.fc_lg]:
            #self._file_portion_box.setValue(0)
            if self._file_openButton.text() == self.fc_dict["open_m"][self.fc_lg]:
                pass
            else:
                self._file_openButton.setText(self.fc_dict["open_m"][self.fc_lg])
        else:pass
        
    #hardware_group
    def _pos_index_info(self,text):
        if text == self.fc_dict["bi-sep"][self.fc_lg]:
            self._file_portion_box.setValue(0)
            if self._file_bind_box.currentText() != self.fc_dict["bind_mul"][self.fc_lg]:
                self._file_bind_box.setCurrentIndex(1)
                self._file_num_box.setEnabled(True)
                self._file_num_box.setMinimum(2)
            else:pass
        else:
            self._file_portion_box.setValue(1)
            if text == self.fc_dict["u_d"][self.fc_lg]:
                self._file_bind_box.setCurrentIndex(0)
                self._file_num_box.setEnabled(False)
            elif text == self.fc_dict["l_r"][self.fc_lg]:
                self._file_bind_box.setCurrentIndex(0)
                self._file_num_box.setEnabled(False)
                self._file_cuc_mark_box.setChecked(False)
                if self._file_type_box.currentIndex() == 0:
                    self._file_tab_mark_box.setChecked(True)
                else:pass                
            else:pass
    #hardware_group    
    def _pos_index_sender(self,text):
        if text == self.fc_dict["u_d"][self.fc_lg]:
            self._file_bind_box.setCurrentIndex(0)
            self._file_num_box.setEnabled(False)
        elif text == self.fc_dict["l_r"][self.fc_lg]:
            self._file_bind_box.setCurrentIndex(0)
            self._file_num_box.setEnabled(False)
            self._file_tab_mark_box.setChecked(True)
            self._file_cuc_mark_box.setChecked(False)
        elif text == self.fc_dict["bi-sep"][self.fc_lg]:
            #self._file_portion_box.setValue(0)
            if self._file_bind_box.currentText()  != self.fc_dict["bind_mul"][self.fc_lg]:
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
            self._file_pos_box.setCurrentIndex(1)
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

