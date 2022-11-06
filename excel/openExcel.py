"""
@author kingfish
创建excel
"""

import xlwings as xw
import os

#启动excel app
app = xw.App(visible=True,add_book=False)

#遍历指定目录下的excel文件，并打开他
filepath = "./excel/datas/"
files = os.listdir(filepath)
print(files)

#遍历目录下以xlsx结尾的文件并打开他
for file in files:
    if file.endswith(".xlsx"):
        app.books.open(file)
    

