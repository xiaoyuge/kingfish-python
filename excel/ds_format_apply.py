"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame
"""

import pandas as pd
import xlwings as xw
import time
import math

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"

read_excel_start = time.time()
#把CP和DS两个sheet的数据分别读入pandas的dataframe
#cp_df = ds_format_workbook.sheets["CP"].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=float).value
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
read_excel_end = time.time()
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")

clear_delta_loi_start = time.time()
#先清空DS表的Delta和LOI列的值
def clear_Delta_Loi(row):
    if row[('Total','Capabity.1')] == 'Delta':
        row[('Current week','BOH')] = 0
    if row[('Total','Capabity.1')] == 'LOI':
        row[('Current week','BOH')] = 0
    
ds_df.apply(clear_Delta_Loi,axis=1)

clear_delta_loi_end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")

cal_delta_loi_start = time.time()
delta_item_group_site_set = set()
loi_item_group_site_set = set()

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def iner_iter_fuc(ds_row_k):
                  
    ds_total_capabity1 = ds_row_k[('Total','Capabity.1')]
        
    #计算DS表的Delta值
    if ds_total_capabity1 == 'Delta':
    #相同的item_group+siteid是否计算过
        if (key in delta_item_group_site_set) == False:
            delta_item_group_site_set.add(key)
            delta_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan((cp_row['MRP (LOI)']))
            MRP_OOI_value = handle_nan(cp_row['MRP (OOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(delta_value,errors='coerce') + pd.to_numeric(MRP_LOI_value,errors='coerce') + pd.to_numeric(MRP_OOI_value,errors='coerce')                        
            print(f"item_group={ds_item_group}-Delta:{ ds_row_k[('Current week','BOH')]}")
    #计算DS表的LOI值
    if ds_total_capabity1 == 'LOI':
        #相同的item_group+siteid是否计算过
        if (key in loi_item_group_site_set) == False:
            loi_item_group_site_set.add(key)
            LOI_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan(cp_row['MRP (LOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
            print(f"item_group={ds_item_group}-LOI:{ ds_row_k[('Current week','BOH')]}")

def iter_in_ds(ds_row):
    
      #获取DS表的Item_group值
        global ds_item_group 
        ds_item_group = ds_row[('Total','Capabity')]
        
        if ds_item_group != "" and cp_item_group == ds_item_group :
            index_j = ds_row.name
            iner_iter_df = ds_df.loc[index_j:index_j+5]
            iner_iter_df.apply(iner_iter_fuc,axis=1)


def iter_in_cp(data):
    global cp_row
    cp_row = data
    #获取CP表的Item_group和siteid值
    global cp_item_group
    cp_item_group = cp_row['Item Group']
    siteid = cp_row['SITEID']
    global key 
    key = cp_item_group + "-" + siteid
    ds_df.apply(iter_in_ds,axis=1)

cp_df.apply(iter_in_cp,axis=1)

#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")

            
