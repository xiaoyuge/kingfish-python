"""
@author kingfish
批量修改excel中sheet的名字
"""

import xlwings as xw

app = xw.App(visible=False,add_book=False)

workbook = app.books.open("excel/rename/统计.xlsx")

for sheet in workbook.sheets:
    sheet.name = sheet.name.replace("销售","")
    
workbook.save()
app.quit()