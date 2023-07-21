"""
@author kingfish
这个代码来源于真实的需求，见data/需求文档.md
先切换工作目录到dt_ds_summary，然后执行该脚本
用pyinstaller打包成exe碰到各种问题，这个文章总结的很好：
https://blog.csdn.net/u012219045/article/details/115397646
"""

import pandas as pd
import xlwings as xw
import time
import math
import openpyxl

#要处理的文件路径
fpath = "data/DT_DS_Summary.xlsm"
#fpath = "DT_DS_Summary.xlsm"#打包exe的时候改成该路径

read_excel_start = time.time()
#把DT_DS_Summary的DT summary、LDT和TDT 三个sheet数据读入内存
dt_summary_df = pd.read_excel(fpath,sheet_name="DT summary",header=[0,1])
ldt_df = pd.read_excel(fpath,sheet_name="LDT",header=[0,1])
tdt_df = pd.read_excel(fpath,sheet_name="TDT",header=[0,1])
read_excel_end = time.time()

#使用xlwings来读取formula
app = xw.App(visible=False,add_book=False)
DT_DS_summary_workbook = app.books.open(fpath)
DT_summary_worksheet = DT_DS_summary_workbook.sheets["DT summary"]
#保留excel中的formula
#获取excel最后一行的索引
excel_last_row_idx = DT_summary_worksheet.used_range.rows.count
#保留最后两列的formula
AN_col_formula = DT_summary_worksheet.range(f'AN3:AN{excel_last_row_idx}').formula
AO_col_formula = DT_summary_worksheet.range(f'AO3:AO{excel_last_row_idx}').formula
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


#先处理一下三个sheet的item_group值，将Nan填充为真实的item_group值
real_ds_item_group = {'key':''}
def handle_nan_item_group_by_row(ds_df_row):
    cur_ds_item_group = ds_df_row[('Total','Capabity')]
    capabity_1 = ds_df_row[('Total','Measure')]
    if type(cur_ds_item_group) == str and cur_ds_item_group != "" :
        real_ds_item_group['key'] = cur_ds_item_group
        return cur_ds_item_group
    elif capabity_1 != 'DOI':
        return real_ds_item_group['key']
    else:
        return ''
        
dt_summary_df[('Total','Capabity')] = dt_summary_df.apply(handle_nan_item_group_by_row,axis=1)
ldt_df[('Total','Capabity')] = ldt_df.apply(handle_nan_item_group_by_row,axis=1)
tdt_df[('Total','Capabity')] = tdt_df.apply(handle_nan_item_group_by_row,axis=1)


clear_summary_delta_loi_start = time.time()
#清空DT Summary表的Delta和LOI列的值
def clear_c_Delta_Loi(row):
    if row[('Total','Measure')] == 'Delta':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Measure')]}的C列值{row[('Current week','BOH')]}")
        return 0
        
    if row[('Total','Measure')] == 'LOI':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Measure')]}的C列值{row[('Current week','BOH')]}")
        return 0

def clear_d_delta(row):
    if row[('Total','Measure')] == 'Delta':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Measure')]}的D列值{row[('last Q ','Rolling')]}")
        return 0
    
dt_summary_df[('Current week','BOH')] = dt_summary_df.apply(clear_c_Delta_Loi,axis=1)
dt_summary_df[('last Q ','Rolling')] = dt_summary_df.apply(clear_d_delta,axis=1)

clear_summary_delta_loi_end = time.time()
print(f"清空DT Summary表的C列Delta和LOI以及D列Delta值 time cost is :{clear_summary_delta_loi_end - clear_summary_delta_loi_start} seconds")

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def Cal_C_Delta_Loi_Iter_In_Row(sum_row,ldt_df,tdt_df):

    sum_item_group = sum_row[('Total','Capabity')]
    sum_b_value = sum_row[('Total','Measure')]
    sum_c_value = sum_row[('Current week','BOH')]

    if sum_b_value == 'Delta':
        ldt_delta = 0
        selected_ldt_rows = ldt_df.loc[(ldt_df[('Total','Capabity')] == sum_item_group) & (ldt_df[('Total','Measure')] == 'Delta'),:]
        for index_row,selected_ldt_row in selected_ldt_rows.iterrows():
            ldt_delta = selected_ldt_row[('Current week','BOH')]
        
        tdt_delta = 0
        selected_tdt_rows = tdt_df.loc[(tdt_df[('Total','Capabity')] == sum_item_group) & (tdt_df[('Total','Measure')] == 'Delta'),:]
        for index_row,selected_tdt_row in selected_tdt_rows.iterrows():
            tdt_delta = selected_tdt_row[('Current week','BOH')]
        return handle_nan(ldt_delta) + handle_nan(tdt_delta)

    if sum_b_value == 'LOI':
        ldt_loi = 0
        selected_ldt_rows = ldt_df.loc[(ldt_df[('Total','Capabity')] == sum_item_group) & (ldt_df[('Total','Measure')] == 'LOI'),:]
        for index_row,selected_ldt_row in selected_ldt_rows.iterrows():
            ldt_loi = selected_ldt_row[('Current week','BOH')]
        
        tdt_loi = 0
        selected_tdt_rows = tdt_df.loc[(tdt_df[('Total','Capabity')] == sum_item_group) & (tdt_df[('Total','Measure')] == 'LOI'),:]
        for index_row,selected_tdt_row in selected_tdt_rows.iterrows():
            tdt_loi = selected_tdt_row[('Current week','BOH')]

        return handle_nan(ldt_loi) + handle_nan(tdt_loi)
    
    return sum_c_value

def Cal_D_Delta_Iter_In_Row(sum_row,ldt_df,tdt_df):
    sum_item_group = sum_row[('Total','Capabity')]
    sum_b_value = sum_row[('Total','Measure')]
    sum_c_value = sum_row[('Current week','BOH')]

    if sum_b_value == 'Delta':
        ldt_delta = 0
        selected_ldt_rows = ldt_df.loc[(ldt_df[('Total','Capabity')] == sum_item_group) & (ldt_df[('Total','Measure')] == 'Delta')]
        for index_row,selected_ldt_row in selected_ldt_rows.iterrows():
            ldt_delta = selected_ldt_row[('last Q ','Rolling')]

        tdt_delta = 0
        selected_tdt_rows = tdt_df.loc[(tdt_df[('Total','Capabity')] == sum_item_group) & (tdt_df[('Total','Measure')] == 'Delta')]
        for index_row,selected_tdt_row in selected_tdt_rows.iterrows():
            tdt_delta = selected_tdt_row[('last Q ','Rolling')]
        return handle_nan(ldt_delta) + handle_nan(tdt_delta)
    
    return sum_c_value

#计算C列的Dela和LOI的值
cal_c_delta_loi_start = time.time()
dt_summary_df[('Current week','BOH')] = dt_summary_df.apply(Cal_C_Delta_Loi_Iter_In_Row,axis=1,args=(ldt_df,tdt_df))
cal_c_delta_loi_end = time.time()
print(f"计算DT Summary表Delta和LOI的C列值 time cost is :{cal_c_delta_loi_end - cal_c_delta_loi_start} seconds")
#计算D列的Dela的值
cal_d_delta_start = time.time()
dt_summary_df[('last Q ','Rolling')] = dt_summary_df.apply(Cal_D_Delta_Iter_In_Row,axis=1,args=(ldt_df,tdt_df))
cal_d_delta_end = time.time()
print(f"计算DT Summary表Delta的D列值 time cost is :{cal_d_delta_end - cal_d_delta_start} seconds")


clear_summary_datetime_start = time.time()

def clear_dt_summary_datetime_value(ds_row,sum_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Measure')]
    if Capabity_1 == 'Demand' or Capabity_1 == 'Supply' or Capabity_1 == 'LOI' or Capabity_1 == 'TTL supply' or Capabity_1 == 'Delta':
        print(f'清空{ds_item_group}的{Capabity_1}的日期{sum_datetime}的值')
        return 0

#清除DT Summary表各个日期的值
for i in range(5,38):
    sum_datetime = dt_summary_df.columns.get_level_values(1)[i]
    sum_month = dt_summary_df.columns.get_level_values(0)[i]
    dt_summary_df[(f'{sum_month}',sum_datetime)] = dt_summary_df.apply(clear_dt_summary_datetime_value,axis=1,args=(sum_datetime,))

clear_summary_datetime_end = time.time()
print(f"清空DT Summary表的日期列的值 time cost is :{clear_summary_datetime_end - clear_summary_datetime_start} seconds")    

cal_summary_datetime_start = time.time()

def cal_dt_summary_by_datetime(ds_row,ds_month,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Measure')]
    datetime_value = ds_row[(ds_month,ds_datetime)]

    if Capabity_1 != 'DOI':

        ldt_value = 0
        selected_ldt_df_rows = ldt_df.loc[(ldt_df[('Total','Capabity')]==ds_item_group) & (ldt_df[('Total','Measure')]==Capabity_1),:]
        for index_selected_row,selected_ldt_df_row in selected_ldt_df_rows.iterrows():
            ldt_value = selected_ldt_df_row[(ds_month,ds_datetime)]

        tdt_value = 0
        selected_tdt_df_rows = tdt_df.loc[(tdt_df[('Total','Capabity')]==ds_item_group) & (tdt_df[('Total','Measure')]==Capabity_1),:]
        for index_selected_row,selected_tdt_df_row in selected_tdt_df_rows.iterrows():
            tdt_value = selected_tdt_df_row[(ds_month,ds_datetime)]

        return_val = handle_nan(ldt_value)+handle_nan(tdt_value)
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_val}")
        return return_val

    return datetime_value

#根据ldt和tdt相同的日期，计算Summary的值
for i in range(5,38):
    ds_datetime = dt_summary_df.columns.get_level_values(1)[i]
    ds_month = dt_summary_df.columns.get_level_values(0)[i]
    dt_summary_df[(f'{ds_month}',ds_datetime)] = dt_summary_df.apply(cal_dt_summary_by_datetime,axis=1,args=(f'{ds_month}',ds_datetime,))

cal_summary_datetime_end = time.time()
print(f"计算DT Sumarry表的datetime的值 time cost is :{cal_summary_datetime_end - cal_summary_datetime_start} seconds")
print(f"DT Sumarry表的datetime的清空和计算总共 time cost is :{cal_summary_datetime_end - clear_summary_datetime_start} seconds")
print(f"dt_ds_summary python 脚本（使用apply）内存计算总共 time cost is :{cal_summary_datetime_end - clear_summary_delta_loi_start} seconds")   

save_excel_start = time.time()
#保存结果到excel       
DT_summary_worksheet.range("A1").expand().options(index=False).value = dt_summary_df
#用之前保留的formulas，重置公式
DT_summary_worksheet.range(f'AN3:AN{excel_last_row_idx}').formula = AN_col_formula
DT_summary_worksheet.range(f'AO3:AO{excel_last_row_idx}').formula = AO_col_formula

DT_DS_summary_workbook.save()
DT_DS_summary_workbook.close()
app.quit()
save_excel_end = time.time()
print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 
print(f"dt_ds_summary python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
