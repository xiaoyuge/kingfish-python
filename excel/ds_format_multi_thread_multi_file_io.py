"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame，并且开启多线程来加速计算
但是该场景是一个CPU密集型场景，python多线程因为GIL的原因，并不能利用到多核加速
所以，本脚本尝试用多线程读取excel，看看是否能够提升读性能
且本脚本尝试把要读取的excel文件先复制一份，用两个线程分别读取两份文件
经测试比多线程读取同一个文件效率有提升
"""

import pandas as pd
import xlwings as xw
import time
import math
from threading import Thread
import threading
import shutil


#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"
#复制的文件路径
cp_fpath = "datas/joyce/DS_format_bak2.xlsm"

def t_read_cp_df(fpath):
    read_cp_df_start = time.time()
    global cp_df
    cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
    read_cp_df_end = time.time()
    print(f"{threading.current_thread().getName()}读取excel文件cp sheet time cost is :{read_cp_df_end - read_cp_df_start} seconds")


def t_read_ds_df(fpath):
    t_read_ds_df_start = time.time()
    global ds_df 
    ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
    t_read_ds_df_end = time.time()
    print(f"{threading.current_thread().getName()}读取excel文件ds sheet time cost is :{t_read_ds_df_end - t_read_ds_df_start} seconds")

def read_excel():
    #先复制一份文件
    cp_excel_start = time.time()
    shutil.copy(fpath,cp_fpath)
    cp_excel_end = time.time()
    print(f"复制文件耗时：{cp_excel_end - cp_excel_start}")
    
    read_excel_start = time.time()
    #把CP和DS两个sheet的数据分别读入pandas的dataframe
    #启动两个线程并行读取两份同样的excel的数据。一个读DS，一个读CP
    read_cp_df_thread = Thread(target=t_read_cp_df,args=(fpath,))
    read_cp_df_thread.start()
    read_ds_df_thread = Thread(target=t_read_ds_df,args=(cp_fpath,))
    read_ds_df_thread.start()

    read_cp_df_thread.join()
    read_ds_df_thread.join()
    read_excel_end = time.time()
    print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")
    print(f"复制和读取excel文件 time cost is :{read_excel_end - cp_excel_start} seconds")

    
def save_excel():
    save_excel_start = time.time()
    #保存结果到excel       
    app = xw.App(visible=False,add_book=False)

    ds_format_workbook = app.books.open(fpath)
    ds_format_workbook.sheets["DS"].range("A3").expand().options(index=False).value = ds_df 

    ds_format_workbook.save()
    ds_format_workbook.close()
    app.quit()
    save_excel_end = time.time()
    print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

delta_item_group_site_set = set()
loi_item_group_site_set = set()

def clear_Delta(row):
    if row[('Total','Capabity.1')] == 'Delta':
        #print(f"线程-{threading.current_thread().getName()}清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
    
def clear_Loi(row):
    if row[('Total','Capabity.1')] == 'LOI':
        #print(f"线程-{threading.current_thread().getName()}清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
    
def clear_Demand(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand':
        #print(f'线程{threading.current_thread().getName()}清空{ds_item_group}的{Capabity_1}的日期{ds_datetime}的值')
        return 0
    
def clear_supply(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Supply':
        #print(f'线程{threading.current_thread().getName()}清空{ds_item_group}的{Capabity_1}的日期{ds_datetime}的值')
        return 0

def Cal_Delta_Iter_In_Ds(ds_row):
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
                #print(f"线程{threading.current_thread().getName()}:item_group={ds_item_group}的Delta={ return_delta_val}")
        return return_delta_val

def Cal_Loi_Iter_In_Ds(ds_row):
     #获取DS表的Item_group值
    ds_item_group = ds_row[('Total','Capabity')]
    #获取DS表的Capabity.1的值，用于判断是delta还是loi
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
        
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
                #print(f"线程{threading.current_thread().getName()}:item_group={ds_item_group}的LOI={ return_LOI_val}")
        return return_LOI_val

def cal_demand_by_datetime(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & (cp_df['Measure']=='Total Publish Demand'),:]
        return_damand_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_damand_val = return_damand_val + cp_df_row[ds_datetime]
        #print(f"线程{threading.current_thread().getName()}:item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_damand_val}")
        return return_damand_val

def cal_supply_by_datetime(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Supply':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & ((cp_df['Measure']=='Total Commit') | (cp_df['Measure']=='Total Risk Commit')),:]
        return_supply_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_supply_val = return_supply_val + cp_df_row[ds_datetime]
        #print(f"线程{threading.current_thread().getName()}:item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_supply_val}")
        return return_supply_val

def p_clear_and_cal_delta():
    #先清除Delta
    ds_df[('Current week','BOH')] = ds_df.apply(clear_Delta,axis=1)
    #计算Delta
    ds_df[('Current week','BOH')] = ds_df.apply(Cal_Delta_Iter_In_Ds,axis=1)
    #释放计算Delta过程中的临时数据
    delta_item_group_site_set.clear()

def p_clear_and_cal_loi():
    #先清除LOI
    ds_df[('Current week','BOH')] = ds_df.apply(clear_Loi,axis=1)
    #计算LOI
    ds_df[('Current week','BOH')] = ds_df.apply(Cal_Loi_Iter_In_Ds,axis=1)
    #释放计算LOI过程中的临时数据
    loi_item_group_site_set.clear()

def p_clear_and_cal_demand():
    #先清除Demand
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_Demand,axis=1,args=(ds_datetime,))
    #计算Demand
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_demand_by_datetime,axis=1,args=(ds_datetime,))

def p_clear_and_cal_supply():
    #先清除Supply
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_supply,axis=1,args=(ds_datetime,))
    #计算Supply
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_supply_by_datetime,axis=1,args=(ds_datetime,))
    
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
    ds_df[('Total','Capabity')] = ds_df.apply(handle_item_group_nan_by_row,axis=1)


if __name__ == "__main__":
    
    app_start = time.time()
    #读取excel数据到内存
    read_excel()
    
    cal_start = time.time()
    #先处理一下item_group的nan值
    handle_item_group_nan()
    #不使用多线程，顺序开始计算
    p_clear_and_cal_delta()
    p_clear_and_cal_loi()
    p_clear_and_cal_demand()
    p_clear_and_cal_supply()
    cal_end = time.time()
    print(f"ds_format python 脚本（使用多线程apply）内存计算总共 time cost is :{cal_end - cal_start} seconds") 
    
    #内存数据写入excel
    save_excel()
    
    app_end = time.time()
    print(f"ds_format python 脚本（使用多线程apply）总共 time cost is :{app_end - app_start} seconds")