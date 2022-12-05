"""
@author kingfish
这个代码来源于真实的需求，见/需求/需求文档.md
先切换工作目录到ds_format，然后执行该脚本
该实现使用Pandas的函数apply()来遍历DataFrame
PS：apply必须通过回调函数的返回值来修改datafram，在回调函数内部对dataframe修改是无效的
"""

import pandas as pd
import xlwings as xw
import time
import math
import openpyxl

#要处理的文件路径
#fpath = "data/DS_format.xlsm"
fpath = "DS_format.xlsm"#打包时候的文件路径

read_excel_start = time.time()
#把CP和DS两个sheet的数据分别读入pandas的dataframe
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
read_excel_end = time.time()
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


#先处理一下DS的item_group值，将Nan填充为真实的item_group值
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
        
ds_df[('Total','Capabity')] = ds_df.apply(handle_nan_item_group_by_row,axis=1)


clear_delta_loi_start = time.time()
#清空DS表的Delta和LOI列的值
def clear_Delta_Loi(row):
    if row[('Total','Capabity.1')] == 'Delta':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
        
    if row[('Total','Capabity.1')] == 'LOI':
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
        
    
ds_df[('Current week','BOH')] = ds_df.apply(clear_Delta_Loi,axis=1)

clear_delta_loi_end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")

cal_delta_loi_start = time.time()
delta_item_group_site_set = set()
loi_item_group_site_set = set()

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def Cal_Delta_Loi_Iter_In_Ds(ds_row):
    
    #获取DS表的Item_group值
    ds_item_group = ds_row[('Total','Capabity')]
    #获取DS表的Capabity.1的值，用于判断是delta还是loi
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
    
    if ds_total_capabity1 == 'Delta':
        return_delta_val = handle_nan(ds_row[('Current week','BOH')])
        #从cp_df获取item_group相等的一组数据
        selected_cp_df = cp_df.loc[cp_df['Item Group']==ds_item_group,:]
        for cp_df_index,cp_df_row in selected_cp_df.iterrows():
            key = cp_df_row['Item Group'] + '-' + cp_df_row['SITEID']
            if (key in delta_item_group_site_set) == False:
                delta_item_group_site_set.add(key)
                MRP_LOI_value = handle_nan((cp_df_row['MRP (LOI)']))
                MRP_OOI_value = handle_nan(cp_df_row['MRP (OOI)'])
                return_delta_val = return_delta_val + pd.to_numeric(MRP_LOI_value,errors='coerce') + pd.to_numeric(MRP_OOI_value,errors='coerce') 
                print(f"item_group={ds_item_group}的Delta={ return_delta_val}")
        return return_delta_val
        
    if ds_total_capabity1 == 'LOI':
        return_LOI_val = handle_nan(ds_row[('Current week','BOH')])
        #从cp_df获取item_group相等的一组数据
        selected_cp_df = cp_df.loc[cp_df['Item Group']==ds_item_group,:]
        for cp_df_index,cp_df_row in selected_cp_df.iterrows():
            key = cp_df_row['Item Group'] + '-' + cp_df_row['SITEID']
            if (key in delta_item_group_site_set) == False:
                LOI_value = handle_nan(ds_row[('Current week','BOH')])
                MRP_LOI_value = handle_nan(cp_df_row['MRP (LOI)'])
                return_LOI_val = return_LOI_val + pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
                print(f"item_group={ds_item_group}的LOI={ return_LOI_val}")
        return return_LOI_val

#计算Dela和LOI的值
ds_df[('Current week','BOH')] = ds_df.apply(Cal_Delta_Loi_Iter_In_Ds,axis=1)

#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")

clear_demand_supply_start = time.time()

def clear_demand_supply(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand' or Capabity_1 == 'Supply':
        print(f'清空{ds_item_group}的{Capabity_1}的日期{ds_datetime}的值')
        return 0

#清除DS表Demand和Supply各个日期的值
#根据DS和CP相同的日期，计算Demand和Supply值
for i in range(5,len(ds_df.columns)):
    ds_datetime = ds_df.columns.get_level_values(1)[i]
    ds_month = ds_df.columns.get_level_values(0)[i]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
        ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_demand_supply,axis=1,args=(ds_datetime,))

clear_demand_supply_end = time.time()
print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end - clear_demand_supply_start} seconds")    

cal_demand_supply_start = time.time()

def cal_demand_supply_by_datetime(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & (cp_df['Measure']=='Total Publish Demand'),:]
        return_damand_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_damand_val = return_damand_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_damand_val}")
        return return_damand_val
    if Capabity_1 == 'Supply':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & ((cp_df['Measure']=='Total Commit') | (cp_df['Measure']=='Total Risk Commit')),:]
        return_supply_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_supply_val = return_supply_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_supply_val}")
        return return_supply_val

#根据DS和CP相同的日期，计算Demand和Supply值
for i in range(5,len(ds_df.columns)):
    ds_datetime = ds_df.columns.get_level_values(1)[i]
    ds_month = ds_df.columns.get_level_values(0)[i]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
        ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_demand_supply_by_datetime,axis=1,args=(ds_datetime,))

cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用apply）内存计算总共 time cost is :{cal_demand_supply_end - clear_delta_loi_start} seconds")   


save_excel_start = time.time()
#保存结果到excel       
app = xw.App(visible=False,add_book=False)

ds_format_workbook = app.books.open(fpath)
ds_format_workbook.sheets["DS"].range("A1").expand().options(index=False).value = ds_df 

ds_format_workbook.save()
ds_format_workbook.close()
app.quit()
save_excel_end = time.time()
print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 
print(f"ds_format python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
