"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame，并且开启多进程来加速计算
结果性能并没有如期加速，反而非常缓慢，分析原因在于manager的dict的性能非常慢
使用shared_memory性能会比dict快10倍，但shared_memory只在Python3.8版本以上支持，且只支持有限的数据类型
我要共享DataFrame行不通
PS:使用Manager，注意在Python3.7版本以上会报freeze_support相关问题
"""
import math
import time
import os
from multiprocessing import Process,Manager,Semaphore

import pandas as pd
import xlwings as xw

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"
df_dict = Manager().dict()

def read_excel():
    #要处理的文件路径
    read_excel_start = time.time()
    #把CP和DS两个sheet的数据分别读入pandas的dataframe
    #cp_df = ds_format_workbook.sheets["CP"].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=float).value
    cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
    ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
    df_dict['ds_df'] = ds_df
    df_dict['cp_df'] = cp_df
    read_excel_end = time.time()
    print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


delta_item_group_site_set = set()
loi_item_group_site_set = set()

    
def save_excel():
    save_excel_start = time.time()
    #保存结果到excel       
    app = xw.App(visible=False,add_book=False)

    ds_format_workbook = app.books.open(fpath)
    ds_format_workbook.sheets["DS"].range("A1").expand().options(index=False).value = df_dict['ds_df']  

    ds_format_workbook.save()
    ds_format_workbook.close()
    app.quit()
    save_excel_end = time.time()
    print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def handle_item_group_nan_by_row(ds_df_row):
    #先处理一下DS的item_group值，将Nan填充为真实的item_group值
    real_ds_item_group = {'key':''}
    cur_ds_item_group = ds_df_row[('Total','Capabity')]
    capabity_1 = ds_df_row[('Total','Capabity.1')]
    if type(cur_ds_item_group) == str and cur_ds_item_group != "" :
        real_ds_item_group['key'] = cur_ds_item_group
        return cur_ds_item_group
    #elif capabity_1 != 'DOI':
    else:
        return real_ds_item_group['key']

def handle_item_group_nan():        
    df_dict['ds_df'][('Total','Capabity')] = df_dict['ds_df'].apply(handle_item_group_nan_by_row,axis=1)

def clear_Delta_Loi_In_DS(row):
    #清空DS表的Delta和LOI列的值
    if row[('Total','Capabity.1')] == 'Delta':
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
        
    if row[('Total','Capabity.1')] == 'LOI':
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0

def Cal_Delta_Loi_Iter_In_Ds(ds_row):
    
    #获取DS表的Item_group值
    ds_item_group = ds_row[('Total','Capabity')]
    #获取DS表的Capabity.1的值，用于判断是delta还是loi
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
    
    if ds_total_capabity1 == 'Delta':
        return_delta_val = handle_nan(ds_row[('Current week','BOH')])
        #从cp_df获取item_group相等的一组数据
        selected_cp_df = df_dict['cp_df'].loc[df_dict['cp_df']['Item Group']==ds_item_group,:]
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
        selected_cp_df = df_dict['cp_df'].loc[df_dict['cp_df']['Item Group']==ds_item_group,:]
        for cp_df_index,cp_df_row in selected_cp_df.iterrows():
            key = cp_df_row['Item Group'] + '-' + cp_df_row['SITEID']
            if (key in delta_item_group_site_set) == False:
                LOI_value = handle_nan(ds_row[('Current week','BOH')])
                MRP_LOI_value = handle_nan(cp_df_row['MRP (LOI)'])
                return_LOI_val = return_LOI_val + pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
                print(f"item_group={ds_item_group}的LOI={ return_LOI_val}")
        return return_LOI_val

def p_clear_and_cal_delta_and_loi():
    #先清除Delta和LOI
    clear_delta_loi_start = time.time()
    df_dict['ds_df'][('Current week','BOH')] = df_dict['ds_df'].apply(clear_Delta_Loi_In_DS,axis=1)
    clear_delta_loi_end = time.time()
    print(f"进程-{os.getpid()}清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")
    #然后计算Delta和LOI
    cal_delta_loi_start = time.time()
    df_dict['ds_df'][('Current week','BOH')] = df_dict['ds_df'].apply(Cal_Delta_Loi_Iter_In_Ds,axis=1)
    cal_delta_loi_end = time.time()
    print(f"进程-{os.getpid()}计算Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")
        

def clear_demand_supply(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand' or Capabity_1 == 'Supply':
        print(f'进程-{os.getpid()}清空{ds_item_group}的{Capabity_1}的日期{ds_datetime}的值')
        return 0


def cal_demand_supply_by_datetime(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand':
        selected_cp_df = df_dict['cp_df'].loc[(df_dict['cp_df']['Item Group']==ds_item_group) & (df_dict['cp_df']['Measure']=='Total Publish Demand'),:]
        return_damand_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_damand_val = return_damand_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_damand_val}")
        return return_damand_val
    if Capabity_1 == 'Supply':
        selected_cp_df = df_dict['cp_df'].loc[(df_dict['cp_df']['Item Group']==ds_item_group) & ((df_dict['cp_df']['Measure']=='Total Commit') | (df_dict['cp_df']['Measure']=='Total Risk Commit')),:]
        return_supply_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_supply_val = return_supply_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_supply_val}")
        return return_supply_val

def p_clear_and_cal_Demand_and_Supply():
    #先清除Demand和Supply
    for i in range(5,len(df_dict['ds_df'].columns)):
        ds_datetime = df_dict['ds_df'].columns.get_level_values(1)[i]
        ds_month = df_dict['ds_df'].columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in df_dict['cp_df'].columns):
            df_dict['ds_df'][(f'{ds_month}',f'{ds_datetime}')] = df_dict['ds_df'].apply(clear_demand_supply,axis=1,args=(ds_datetime,))
    #计算Demand和Supply
    for i in range(5,len(df_dict['ds_df'].columns)):
        ds_datetime = df_dict['ds_df'].columns.get_level_values(1)[i]
        ds_month = df_dict['ds_df'].columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in df_dict['cp_df'].columns):
            df_dict['ds_df'][(f'{ds_month}',f'{ds_datetime}')] = df_dict['ds_df'].apply(cal_demand_supply_by_datetime,axis=1,args=(ds_datetime,))
    

if __name__ == '__main__':
    
    print(f"Process-{os.getpid()} is running...")
    app_start = time.time()
    
    #读取excel数据到内存
    read_excel()
    
    #先处理一下item_group的nan值
    handle_item_group_nan()
    
    #因为我的Mac本cpu是双核的，所以起两个进程计算
    cal_start = time.time()
    p_cal_delta_loi = Process(target=p_clear_and_cal_delta_and_loi,args=())
    p_cal_demand_supply = Process(target=p_clear_and_cal_Demand_and_Supply,args=())
    
    p_cal_delta_loi.start()
    p_cal_demand_supply.start()
    
    p_cal_delta_loi.join()
    p_cal_demand_supply.join()
    
    cal_end = time.time()
    print(f"ds_format python 脚本（使用多进程apply）内存计算总共 time cost is :{cal_end - cal_start} seconds") 
    
    #内存数据写入excel
    save_excel()
    
    app_end = time.time()
    print(f"ds_format python 脚本（使用多进程apply）总共 time cost is :{app_end - app_start} seconds")