"""
@author Kingfish
一个excel中多个sheets间进行vlookup
"""

import pandas as pd
import xlwings as xw

app = xw.App(visible=False,add_book=False)

#要操作的表的目录路径
fpath = "datas/multi_excel_sheets_vlookup/"

score_workbook = app.books.open(fpath+"成绩表数据.xlsx")

#获取成绩表第一个sheet的数据
score_total_df = score_workbook.sheets[0].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=int).value

print("*"*50)
print(score_total_df)

#用来放学生信息dataframe
student_dfs = []

#获取成绩表从sheet1开始往后的sheets
for student_sheet in list(score_workbook.sheets)[1:]:
    student_df = student_sheet.range("A1").options(pd.DataFrame,expand='table',index=False,numbers=int).value
    #给数据加一列班级
    class_ = {
        "一班同学录":"一班",
        "二班同学录":"二班",
        "三班同学录":"三班",
        "四班同学录":"四班",
        "五班同学录":"五班"
    }[student_sheet.name]
    student_df["班级"] = class_
    student_dfs.append(student_df)
 
#把学生信息合并到一起
student_df = pd.concat(student_dfs)   
print("*"*50)
print(student_df)

#根据班级和姓名两个字段进行Merge
merge_df = pd.merge(score_total_df,student_df,left_on=["班级","姓名"],right_on=["班级","姓名"])

#复制电话列的值为电话号码列的值
merge_df["电话号码"] = merge_df["电话"]
#删除电话号码列
merge_df.drop("电话",axis=1,inplace=True)

print("*"*50)
print(merge_df)

#把结果写入第一个sheet
score_workbook.sheets[0].range("A1").options(index=False).value = merge_df

score_workbook.save()
score_workbook.close()
app.quit()





