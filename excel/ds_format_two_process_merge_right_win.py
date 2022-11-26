"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame，并且开启多进程来加速计算
本方案不用多进程间通信的方式，改为多个进程分开计算，然后内存直接合并，再输出到文件的方式
同样的代码在macos上执行没问题，在win上执行报错，因此不用manager来管理同步，改用queue
使用queue需要注意，queue.put调用一次后，需要get后才能再次put，而且如果不是在process.join之前调用get，
那么会一直阻塞
"""

import math
import time
from multiprocessing import Process,Manager,Queue

import pandas as pd
import xlwings as xw
import os

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"
#dict = Manager().dict()

def read_excel():
    #要处理的文件路径
    read_excel_start = time.time()
    #把CP和DS两个sheet的数据分别读入pandas的dataframe
    global cp_df 
    cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0],engine='openpyxl')
    global ds_df 
    ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1],engine='openpyxl')
    read_excel_end = time.time()
    print(f"进程-{os.getpid()}读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


delta_item_group_site_set = set()
loi_item_group_site_set = set()

    
def save_excel(result_df):
    #保存结果到excel       
    app = xw.App(visible=False,add_book=False)

    ds_format_workbook = app.books.open(fpath)
    ds_format_workbook.sheets["DS"].range("A1").expand().options(index=False).value = result_df

    ds_format_workbook.save()
    ds_format_workbook.close()
    app.quit()

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data


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

def handle_nan_item_group():
    ds_df[('Total','Capabity')] = ds_df.apply(handle_nan_item_group_by_row,axis=1)

 #清空DS表的Delta和LOI列的值
def clear_Delta_Loi(row):
    if row[('Total','Capabity.1')] == 'Delta':
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0
            
    if row[('Total','Capabity.1')] == 'LOI':
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
        return 0

delta_item_group_site_set = set()
loi_item_group_site_set = set()

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
                #print(f"item_group={ds_item_group}的Delta={ return_delta_val}")
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
                #print(f"item_group={ds_item_group}的LOI={ return_LOI_val}")
        return return_LOI_val


def p_clear_and_cal_delta_loi(q):
    #读取excel数据到内存
    read_excel()
    #先处理一下item_group的nan值
    handle_nan_item_group()
    #清空开始
    clear_delta_loi_start = time.time()
    ds_df[('Current week','BOH')] = ds_df.apply(clear_Delta_Loi,axis=1)
    clear_delta_loi_end = time.time()
    print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")
    #计算开始
    cal_delta_loi_start = time.time()
    #计算Dela和LOI的值
    ds_df[('Current week','BOH')] = ds_df.apply(Cal_Delta_Loi_Iter_In_Ds,axis=1)
    q.put(ds_df)
    #dict['ds_delta_loi'] = ds_df
    #释放数据
    delta_item_group_site_set.clear()
    loi_item_group_site_set.clear()
    cal_delta_loi_end = time.time()
    print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")


def clear_demand_supply(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand' or Capabity_1 == 'Supply':
        #print(f'清空{ds_item_group}的{Capabity_1}的日期{ds_datetime}的值')
        return 0

def cal_demand_supply_by_datetime(ds_row,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if Capabity_1 == 'Demand':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & (cp_df['Measure']=='Total Publish Demand'),:]
        return_damand_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_damand_val = return_damand_val + cp_df_row[ds_datetime]
        #print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_damand_val}")
        return return_damand_val
    if Capabity_1 == 'Supply':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & ((cp_df['Measure']=='Total Commit') | (cp_df['Measure']=='Total Risk Commit')),:]
        return_supply_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_supply_val = return_supply_val + cp_df_row[ds_datetime]
        #print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_datetime}的值={return_supply_val}")
        return return_supply_val

def p_clear_and_cal_demand_supply(q):
    #读取excel数据到内存
    read_excel()
    #先处理一下item_group的nan值
    handle_nan_item_group()
    clear_demand_supply_start = time.time()
    #根据DS和CP相同的日期，计算Demand和Supply值
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_demand_supply,axis=1,args=(ds_datetime,))
    clear_demand_supply_end = time.time()
    print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end - clear_demand_supply_start} seconds")  
    #计算开始
    cal_demand_supply_start = time.time()
    #根据DS和CP相同的日期，计算Demand和Supply值
    for i in range(5,len(ds_df.columns)):
        ds_datetime = ds_df.columns.get_level_values(1)[i]
        ds_month = ds_df.columns.get_level_values(0)[i]
        if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_df.columns):
            ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_demand_supply_by_datetime,axis=1,args=(ds_datetime,))
    cal_demand_supply_end = time.time()
    q.put(ds_df)
    #dict['ds_demand_supply'] = ds_df
    print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
    print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")

def merge_delta_loi_to_demand_supply_apply(ds_df_demand_supply_row,ds_df_delta_loi):
    item_group = ds_df_demand_supply_row[('Total','Capabity')]
    capabity_1 = ds_df_demand_supply_row[('Total','Capabity.1')]
    if capabity_1 == 'Delta' or capabity_1 == 'LOI': 
        selected_rows = ds_df_delta_loi.loc[(ds_df_delta_loi[('Total','Capabity')]==item_group) & (ds_df_delta_loi[('Total','Capabity.1')]==capabity_1),:]
        for index_selected_row,selected_row in selected_rows.iterrows():
            #应该只有一行
            return selected_row[('Current week','BOH')]
        
        

def merge_delta_loi_to_demand_supply(ds_df_delta_loi,ds_df_demand_supply):
    ds_df_demand_supply[('Current week','BOH')] = ds_df_demand_supply.apply(merge_delta_loi_to_demand_supply_apply,axis=1,args=(ds_df_delta_loi,))


if __name__ == '__main__':
   
    print(f"主进程-{os.getpid()} is running...")
    
    cal_start = time.time()

    delta_loi_q = Queue()
    demand_supply_q = Queue()
   
    #这里起两个进程，一个计算Delta和LOI，一个计算Demand和Supply
    p_cal_delta_loi = Process(target=p_clear_and_cal_delta_loi,args=(delta_loi_q,))
    p_cal_demand_supply = Process(target=p_clear_and_cal_demand_supply,args=(demand_supply_q,))
    
    p_cal_delta_loi.start()
    p_cal_demand_supply.start()

    ds_df_delta_loi = delta_loi_q.get()
    p_cal_delta_loi.join()
   
    ds_df_demand_supply = demand_supply_q.get()
    p_cal_demand_supply.join()
    
    cal_end = time.time()
    print(f"ds_format python 脚本（使用多进程apply）读取数据+内存计算总共 time cost is :{cal_end - cal_start} seconds") 
    
    #将ds_delta_loi合并到ds_demand_supply
    merge_start = time.time()
    merge_delta_loi_to_demand_supply(ds_df_delta_loi,ds_df_demand_supply)
    merge_end = time.time()
    print(f"将内存计算结果进行合并time cost is :{merge_end - merge_start} seconds")
    
    #将内存计算结果保存到excel
    save_start = time.time()
    save_excel(ds_df_demand_supply)
    save_end = time.time()
    print(f"将内存结果保存到excel总共 time cost is :{save_end - save_start} seconds")
    print(f"ds_format python 脚本（使用多进程apply）总共 time cost is :{save_end - cal_start} seconds")
