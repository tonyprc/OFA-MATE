# OFA-MATE

# 傲飞伴侣：一对多平行语料格式转换工具
## OFA-MATE: One to Many Corpus Format Converter for OFA-ParaConc

### 软件概况
### GENERAL INFO

傲飞伴侣（OFA-Mate）是为一对多平行语料检索软件OFA-ParaConc量身定制的语料格式转换软件，可将常见的文本文件（txt）、WORD文档（docx）及EXCEL文档（xlsx）格式的双语语料转换成符合ParaConc检索基本要求的json格式。本软件编写语言为python 3.8，UTF8编码，采用PyInstaller进行打包。本版本目前可在windows 7+窗口环境下运行(64位)。打包文件内含app_data、samples及savedfiles三个工作目录，请勿擅自增删相关文件，以免影响软件的正常运行。
本软件内含的各类sample文档基本代表了可直接用于本软件执行转码操作的常见语料格式。

As a corpus format converter customized for OFA-ParaConc, OFA-Mate aims to convert bilingual corpus files in formats of txt, docx, or xlsx into json. It is also compiled in python 3.8, encoded in UTF-8 and packed by PyInstaller for windows 7+ platforms only at the moment. It consists of three working directories, among which you can find enough corpus samples for a good understanding on what kind of corpus file this tool can handle well.

---

### 基本功能
### FUNCTIONS

1. 语料读取
1. DATA READING
2. 自动填充
2. AUTO FILLING
3. 操作提示
3. OPERATION PROMPT
4. 转码输出
4. CONVERT & OUTPUT

#### 语料读取
#### DATA READING

语料读取功能方便用户根据具体需求自行加载符合转码格式的双语语料单文件或多文件。单文件指原、译文均在一个文件之内；多文件指原、译文分文件单独存贮。

This function allows users to feed bi-language files or mono-language files to the tool. A bi-language file refers to a file that contains both the SL text and the TL text; a group of mon-language files refers to files where SL and TL texts are stored seperately.

使用方法：启动软件，按窗体顶部的操作提示先选择“文档类型”（txt, docx, xlsx），再选择“组合方式”（单文件，多文件），然后点击“打开单文件”（或“打开多文件”），找到自己要进行转码的语料单文件（或整个文件夹），然后点击“确定”即可。

USAGE: Run the tool, read the promts in the upper part of the window, choose "file type" among txt, docx, and xlsx, choose "bind type" between single file and multi-files,
and then click "Open Single File" (or "Open Multi Files"), pick out the file or the directory for converting, and finally click the "open" button.

#### 自动填充
#### AUTO FILLING
自动填充功能方便用户快速完成双语语料元信息标注及有可能缺失的对齐基本标记项的填加。元信息标注项包括标题，作者，译者，语言，日期，版本号，类型等七项，对齐基本标记项包括统一行号，对齐句段，篇章标题等三项。

The function aims to free user's hands from the tedious jobs of adding meta information or missing columns for each corpus file. The necessary meta information for OFA ParaConc includes "title", "author", "translator", "language", "date", "version", and "genre", and the three basic columns for each corpus file are "Sent Number", "Sent", and "Chapter or Single Text Title".

使用方法：在上一步点击了“确定”后，本工具即时启动自动填充功能， 并将从所加载语料中提取到的各类标注项直接填加到源语语料及目标语语料表格窗口当中，同时校正其上的检索标记项。
用户可补加或修正自动填充功能未能填写或填写错误的标记项。

USAGE: The click of the "open" button will activate the auto-filling function immediately, outputing all the meta info or missing columns it found within the corpus to the display window of SL Corpus Preview and TL Corpus Preview. It will also readjust the various corpus noting parameters in the upper window. However, "Even Homer nods!". It's necessary for users to check each filled or unfilled item to make sure that the information is 100% correct.

#### 操作提示
#### OPERATION PROMPTS

操作提示功能方便用户了解界面各组件基本功能及把握语料转码进程。提示信息以操作提示窗口、悬浮文字及状态栏文字等三种方式进行展示。

This function helps users to be familiar with the tool and keep trace of the converting process. Various prompts may appear in the Operation Prompts Window, pop_up word frames, or the status bar.

使用方法：有关每次操作的提示都将出现在窗体顶部的操作提示窗口中；操作结果或错误信息等将出现在窗体底部的状态栏内；将鼠标置于某组件之上并停留片刻，即可看到相应组件的基本功能提示信息。

USAGE: Prompts for Converting steps will appear in the the Operation Prompts Window in the upper part of the window; Cheers or Errors will be prompted in the status bar; what's-this prompts will pop up automatically when you put your mouse cursor right above certain component of the tool.

#### 转码输出
#### CONVERT & OUTPUT

转码输出功能方便用户获取所需json文件以供OFA-ParaConc检索使用。

This function enables users to fetch the json files that are, without any doubt, "needy" for OFA-ParaConc. 

使用方法：当操作提示通知您“所有语料均已提交完毕”，并提醒您点击“转换格式”按钮时，点击窗体右下角的“转换格式”按钮，然后按出现的操作提示到相应目录中查收最后生成的json文件即可。

USAGE: When the prompt reads like "all files have be submitted successfully" or "please click the 'Converting' button now", you need to find the button in the lower right corner of the window and click it. After that, find the json file in the directory it is supposed to be and transfer it to the corpus directory of OFA-ParaConc, and Cheers!

### 搭建运行环境
### Set Up the Environment

#### 第三方库列表
#### Third-Party Programs List

[requirements.txt](requirements.txt) 

#### 打包软件安装
#### Install the Packaging Tool

`> pip install pyinstaller`

#### 程序打包
#### Pack This Program
`> pyinstaller -F -w main.py`

---

### 致谢
### ACKNOWLEDGEMENT

本软件的完成实在离不开以下人员的关心与帮助，在此一并表示由衷的感谢：
感谢河南城建学院李攀登先生对本人的激励、建议与一贯的支持；
感谢赵SIR对本软件进行的专业化结构调整与打磨；
感谢沈阳药科大学肇彤女士的前期研究成果及支持；
感谢微信公众号版主爱德宝器先生对本人的鼓舞与支持；
感谢“一心一译”翻译组各位师友给予的灵感、信任与关爱；
感谢本系主任张秀红教授对本软件开发及本人身心健康的长期关切；
同时也向AntConc，BFSU ParaConc及CUC的开发者们致以崇高的敬意。
最后再容我感谢一下我的家人的体谅、支持与期望。

All the following people are indispensible for the accomplishment of this little software, and my heartfelt thanks go directly to all of them:
Many thanks to Gordon from Henan City Construction College for his suggests, encouragement and long-lasting supports;
Many thanks to Mr. Zhao for his professional readjustment and polish of this shabby program;
Many thanks to Mz. Zhao Tong for her previous study in this area as well as her firm supports;
Many thanks to my friend, AiDeBaoQi, who gives me the faith in writing programs as a green hand together with selfless supports; 
Many thanks to scholars, teachers as well as brothers and sisters in the translation group of "One Heart One Mind" for almost everything within this software;
Many thanks to Prof. Linda Zhang, dean of the Foreign Languages Department of Fushun Vocational Technology Institute (Fushun Teacher's College) for her great concern with my works as well as my health;
Special thanks and respects go to all the developers of AntConc, BFSU ParaConc and CUC.
Last but not the least, allow me to give thanks to my beloved family, many many thanks!

---

### 软件图标
### My Icon
![](./app_data/workfiles/myIcon.png)  

