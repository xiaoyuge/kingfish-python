"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
"""

import pandas as pd
import xlwings as xw
import time
import math

#要处理的文件路径
fpath = "datas/joyce/LNB_summary_format.xlsm"

read_excel_start = time.time()
#把LNB_summary_format的Summary、SD和OBsheet数据读入内存
summary_df = pd.read_excel(fpath,sheet_name="LNB summary",header=[0,1])
sd_df = pd.read_excel(fpath,sheet_name="SD",header=[0,1])
ob_df = pd.read_excel(fpath,sheet_name="OB",header=[0,1])
read_excel_end = time.time()
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


#先处理一下三个sheet的item_group值，将Nan填充为真实的item_group值
real_ds_item_group = {'key':''}
def handle_nan_item_group_by_row(ds_df_row):
    cur_ds_item_group = ds_df_row[('Total','Capabity')]
    capabity_1 = ds_df_row[('Total','Capabity.1')]
    if type(cur_ds_item_group) == str and cur_ds_item_group != "" :
        real_ds_item_group['key'] = cur_ds_item_group
        return cur_ds_item_group
    elif capabity_1 != 'DOI':
        return real_ds_item_group['key']
    else:
        return ''
        
summary_df[('Total','Capabity')] = summary_df.apply(handle_nan_item_group_by_row,axis=1)
sd_df[('Total','Capabity')] = sd_df.apply(handle_nan_item_group_by_row,axis=1)
ob_df[('Total','Capabity')] = ob_df.apply(handle_nan_item_group_by_row,axis=1)


clear_summary_delta_loi_start = time.time()
#清空Summary表的Delta和LOI列的值
def clear_c_Delta_Loi(row):
    if row[('Total','Capabity.1')] == 'Delta':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的C列值{row[('Current week','BOH')]}")
        return 0
        
    if row[('Total','Capabity.1')] == 'LOI':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的C列值{row[('Current week','BOH')]}")
        return 0

def clear_d_delta(row):
    if row[('Total','Capabity.1')] == 'Delta':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的D列值{row[('Sep end ','Rolling')]}")
        return 0
    
summary_df[('Current week','BOH')] = summary_df.apply(clear_c_Delta_Loi,axis=1)
summary_df[('Sep end ','Rolling')] = summary_df.apply(clear_d_delta,axis=1)

clear_summary_delta_loi_end = time.time()
print(f"清空Summary表的C列Delta和LOI以及D列Delta值 time cost is :{clear_summary_delta_loi_end - clear_summary_delta_loi_start} seconds")

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def Cal_C_Delta_Loi_Iter_In_Row(sum_row,sd_df,ob_df):

    sum_item_group = sum_row[('Total','Capabity')]
    sum_b_value = sum_row[('Total','Capabity.1')]
    sum_c_value = sum_row[('Current week','BOH')]

    if sum_b_value == 'Delta':
        sd_delta = 0
        selected_sd_rows = sd_df.loc[(sd_df[('Total','Capabity')] == sum_item_group) & (sd_df[('Total','Capabity.1')] == 'Delta'),:]
        for index_row,selected_sd_row in selected_sd_rows.iterrows():
            sd_delta = selected_sd_row[('Current week','BOH')]
        
        ob_delta = 0
        selected_ob_rows = ob_df.loc[(ob_df[('Total','Capabity')] == sum_item_group) & (ob_df[('Total','Capabity.1')] == 'Delta'),:]
        for index_row,selected_ob_row in selected_ob_rows.iterrows():
            ob_delta = selected_ob_row[('Current week','BOH')]
        return handle_nan(sd_delta) + handle_nan(ob_delta)

    if sum_b_value == 'LOI':
        sd_loi = 0
        selected_sd_rows = sd_df.loc[(sd_df[('Total','Capabity')] == sum_item_group) & (sd_df[('Total','Capabity.1')] == 'LOI'),:]
        for index_row,selected_sd_row in selected_sd_rows.iterrows():
            sd_loi = selected_sd_row[('Current week','BOH')]
        
        ob_loi = 0
        selected_ob_rows = ob_df.loc[(ob_df[('Total','Capabity')] == sum_item_group) & (ob_df[('Total','Capabity.1')] == 'LOI'),:]
        for index_row,selected_ob_row in selected_ob_rows.iterrows():
            ob_loi = selected_ob_row[('Current week','BOH')]

        return handle_nan(sd_loi) + handle_nan(ob_loi)
    
    return sum_c_value

def Cal_D_Delta_Iter_In_Row(sum_row,sd_df,ob_df):
    sum_item_group = sum_row[('Total','Capabity')]
    sum_b_value = sum_row[('Total','Capabity.1')]
    sum_c_value = sum_row[('Current week','BOH')]

    if sum_b_value == 'Delta':
        sd_delta = 0
        selected_sd_rows = sd_df.loc[(sd_df[('Total','Capabity')] == sum_item_group) & (sd_df[('Total','Capabity.1')] == 'Delta')]
        for index_row,selected_sd_row in selected_sd_rows.iterrows():
            sd_delta = selected_sd_row[('Sep end ','Rolling')]

        ob_delta = 0
        selected_ob_rows = ob_df.loc[(ob_df[('Total','Capabity')] == sum_item_group) & (ob_df[('Total','Capabity.1')] == 'Delta')]
        for index_row,selected_ob_row in selected_ob_rows.iterrows():
            ob_delta = selected_ob_row[('Sep end ','Rolling')]
        return handle_nan(sd_delta) + handle_nan(ob_delta)
    
    return sum_c_value

#计算C列的Dela和LOI的值
cal_c_delta_loi_start = time.time()
summary_df[('Current week','BOH')] = summary_df.apply(Cal_C_Delta_Loi_Iter_In_Row,axis=1,args=(sd_df,ob_df))
cal_c_delta_loi_end = time.time()
print(f"计算Summary表Delta和LOI的C列值 time cost is :{cal_c_delta_loi_end - cal_c_delta_loi_start} seconds")
#计算D列的Dela的值
cal_d_delta_start = time.time()
summary_df[('Sep end ','Rolling')] = summary_df.apply(Cal_D_Delta_Iter_In_Row,axis=1,args=(sd_df,ob_df))
cal_d_delta_end = time.time()
print(f"计算Summary表Delta的D列值 time cost is :{cal_d_delta_end - cal_d_delta_start} seconds")


clear_summary_datetime_start = time.time()

def clear_lnb_summary_datetime_value(ds_row,sum_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand' or Capabity_1 == 'Supply' or Capabity_1 == 'LOI' or Capabity_1 == 'TTL supply' or Capabity_1 == 'Delta':
        print(f'清空{ds_item_group}的{Capabity_1}的日期{sum_datetime}的值')
        return 0

#清除LNB Summary表各个日期的值
for i in range(5,38):
    sum_datetime = summary_df.columns.get_level_values(1)[i]
    sum_month = summary_df.columns.get_level_values(0)[i]
    summary_df[(f'{sum_month}',sum_datetime)] = summary_df.apply(clear_lnb_summary_datetime_value,axis=1,args=(sum_datetime,))

clear_summary_datetime_end = time.time()
print(f"清空Summary表的日期列的值 time cost is :{clear_summary_datetime_end - clear_summary_datetime_start} seconds")    

cal_summary_datetime_start = time.time()

def cal_summary_by_datetime(ds_row,ds_month,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    datetime_value = ds_row[(ds_month,ds_datetime)]

    if Capabity_1 != 'DOI':

        sd_value = 0
        selected_sd_df_rows = sd_df.loc[(sd_df[('Total','Capabity')]==ds_item_group) & (sd_df[('Total','Capabity.1')]==Capabity_1),:]
        for index_selected_row,selected_sd_df_row in selected_sd_df_rows.iterrows():
            sd_value = selected_sd_df_row[(ds_month,ds_datetime)]

        ob_value = 0
        selected_ob_df_rows = ob_df.loc[(ob_df[('Total','Capabity')]==ds_item_group) & (ob_df[('Total','Capabity.1')]==Capabity_1),:]
        for index_selected_row,selected_ob_df_row in selected_ob_df_rows.iterrows():
            ob_value = selected_ob_df_row[(ds_month,ds_datetime)]

        return_val = handle_nan(sd_value)+handle_nan(ob_value)
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_val}")
        return return_val
        
    return datetime_value

#根据SD和OB相同的日期，计算Summary的值
for i in range(5,38):
    ds_datetime = summary_df.columns.get_level_values(1)[i]
    ds_month = summary_df.columns.get_level_values(0)[i]
    summary_df[(f'{ds_month}',ds_datetime)] = summary_df.apply(cal_summary_by_datetime,axis=1,args=(f'{ds_month}',ds_datetime,))

cal_summary_datetime_end = time.time()
print(f"计算DS表的datetime的值 time cost is :{cal_summary_datetime_end - cal_summary_datetime_start} seconds")
print(f"DS表的datetime的清空和计算总共 time cost is :{cal_summary_datetime_end - clear_summary_datetime_start} seconds")
print(f"ds_format python 脚本（使用apply）内存计算总共 time cost is :{cal_summary_datetime_end - clear_summary_delta_loi_start} seconds")   

save_excel_start = time.time()
#保存结果到excel       
app = xw.App(visible=False,add_book=False)

ds_format_workbook = app.books.open(fpath)
ds_format_workbook.sheets["LNB summary"].range("A1").expand().options(index=False).value = summary_df

ds_format_workbook.save()
ds_format_workbook.close()
app.quit()
save_excel_end = time.time()
print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 
print(f"ds_format python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
