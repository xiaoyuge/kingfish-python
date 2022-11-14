"""
@author kingfish
对多个excel文件进行vlookup
"""

import os
import pandas as pd
import xlwings as xw

#要操作的文件所在的目录路径
score_fpath = "datas/multi_excel_vlookup/"
student_info_fpath = "datas/multi_excel_vlookup/student_info/"

#存放多个文件合并后的数据
dfs = []

#读取目标目录下的文件
files = os.listdir(student_info_fpath)

for file in files:
    if file.startswith("~$") == False and file.endswith("同学录.xlsx"):
        student_info_df = pd.read_excel(student_info_fpath+file,header=0)
        #给数据添加班级列，文件名前两个字符是班级
        student_info_df["班级"] = file[0:2]
        #另外一种取班级的方法：student_info_df["班级"] = file.replace("同学录.xlsx","")
        dfs.append(student_info_df)

#将多个文件合并到一起
student_info_df = pd.concat(dfs)
print("*"*50)
print(student_info_df)

#读取成绩表数据
#直接用pandas的reaad_Excel读取excel数据，有时会碰到一些文件格式兼容性的问题，建议还是用专门的excel库比如xlwings来处理
score_df = pd.read_excel(score_fpath+"成绩表数据.xlsx",header=0)
print("*"*50)
print(score_df)

#根据姓名和班级两个字段做vlookup
merge_df = pd.merge(student_info_df,score_df,left_on=["姓名","班级"],right_on=["姓名","班级"])
print("*"*50)
print(merge_df)

#对合并后的数据，将电话号码列复制为电话列
merge_df["电话号码"] = merge_df["电话"]
#inplace这个参数比较关键，为true即在当前df内操作，为false返回一个新的df
merge_df.drop("电话",axis=1,inplace=True)
print("*"*50)
print(merge_df)

app = xw.App(visible=False,add_book=False)

workbook_score = app.books.open(score_fpath+"成绩表数据_new.xlsx")

workbook_score.sheets[0].range("A1").options(index=False).value = merge_df

workbook_score.save()
workbook_score.close()
app.quit()
    





