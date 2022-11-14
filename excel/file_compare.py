"""
@author Kingfish

比较两个excel的不同之处，并标颜色
"""

import xlwings as xw


app = xw.App(visible=False,add_book=False)

workbook_student = app.books.open("datas/student_excel/student_excel_clean.xlsx")
workbook_student_compare = app.books.open("datas/student_excel/student_excel_modify.xlsx")

for row in workbook_student.sheets[0].range("A1").expand():
    for cell in row:
            cell_compare = workbook_student_compare.sheets[0].range(cell.address)
            if cell.value != cell_compare.value:
                cell.color = cell_compare.color = (255,0,0)
                
workbook_student.save()
workbook_student_compare.save()
workbook_student.close()
workbook_student_compare.close()
app.quit()
            