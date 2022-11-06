"""
@author kingfish
创建excel
"""

import xlwings as xw
import os

#打开excel app
app = xw.App(visible=False,add_book=False)

#批量创建一批excel文件
for dept in ['技术部','产品部','运营部','销售部','财务部']:
    workbook = app.books.add()
    workbook.save(f"./excel/create/部门业绩-{dept}.xlsx")

