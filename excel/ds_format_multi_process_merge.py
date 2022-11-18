"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame，并且开启多进程来加速计算
本方案不用多进程间通信的方式，改为多个进程分开计算，然后内存直接合并，再输出到文件的方式
但该方案还是错误的使用了apply()方法，是错误示范，正确方案见
"""

import math
import time
from multiprocessing import Process,Manager

import pandas as pd
import xlwings as xw
import os

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"

dict = Manager().dict()

def read_excel():
    #要处理的文件路径
    read_excel_start = time.time()
    #把CP和DS两个sheet的数据分别读入pandas的dataframe
    global cp_df 
    cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0],engine='openpyxl')
    global ds_df 
    ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1],engine='openpyxl')
    read_excel_end = time.time()
    print(f"进程-{os.getpid}读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


delta_item_group_site_set = set()
loi_item_group_site_set = set()

    
def save_excel(result_df):
    save_excel_start = time.time()
    #保存结果到excel       
    app = xw.App(visible=False,add_book=False)

    ds_format_workbook = app.books.open(fpath)
    ds_format_workbook.sheets["DS"].range("A3").expand().options(index=False).value = result_df

    ds_format_workbook.save()
    ds_format_workbook.close()
    app.quit()
    save_excel_end = time.time()
    print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

#############################################Delta和Loi计算####################################################



def iner_Iter_From_Cal_loi_Iter_In_Ds(ds_row_k):
    ds_total_capabity1 = ds_row_k[('Total','Capabity.1')]
    if ds_total_capabity1 == 'LOI':
        #相同的item_group+siteid是否计算过
        if (cal_loi_key in loi_item_group_site_set) == False:
            loi_item_group_site_set.add(cal_loi_key)
            LOI_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan(cal_loi_cp_row['MRP (LOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
            print(f"item_group={cal_loi_ds_item_group}的LOI={ ds_row_k[('Current week','BOH')]}")

def Cal_Loi_Iter_In_Ds(ds_row):
     #获取DS表的Item_group值
    global cal_loi_ds_item_group 
    cal_loi_ds_item_group = ds_row[('Total','Capabity')]
        
    if cal_loi_ds_item_group != "" and cal_loi_cp_item_group == cal_loi_ds_item_group :
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+5]
        iner_iter_df.apply(iner_Iter_From_Cal_loi_Iter_In_Ds,axis=1)
    

def Cal_Loi_Iter_In_Cp(cp_row):
    global cal_loi_cp_row
    cal_loi_cp_row = cp_row
    #获取CP表的Item_group和siteid值
    global cal_loi_cp_item_group
    cal_loi_cp_item_group = cal_loi_cp_row['Item Group']
    siteid = cal_loi_cp_row['SITEID']
    global cal_loi_key 
    cal_loi_key = cal_loi_cp_item_group + "-" + siteid
    ds_df.apply(Cal_Loi_Iter_In_Ds,axis=1)
    

def iner_Iter_From_Cal_Delta_Iter_In_Ds(ds_row_k):
    
    ds_total_capabity1 = ds_row_k[('Total','Capabity.1')]
    ds_total_capabity = ds_row_k[('Total','Capabity')]
    
    #因为合并单元格的原因，只有第一行有值，其他行为Nan，为方便后续处理，将Nan的行都填充值
    if ds_total_capabity == "":
        ds_row_k[('Total','Capabity')] = cal_delta_ds_item_group
        
    #计算DS表的Delta值
    if ds_total_capabity1 == 'Delta':
    #相同的item_group+siteid是否计算过
        if (cal_delta_key in delta_item_group_site_set) == False:
            delta_item_group_site_set.add(cal_delta_key)
            delta_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan((cal_delta_cp_row['MRP (LOI)']))
            MRP_OOI_value = handle_nan(cal_delta_cp_row['MRP (OOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(delta_value,errors='coerce') + pd.to_numeric(MRP_LOI_value,errors='coerce') + pd.to_numeric(MRP_OOI_value,errors='coerce')                        
            print(f"item_group={cal_delta_ds_item_group}的Delta={ ds_row_k[('Current week','BOH')]}")
    

def cal_Delta_Iter_In_Ds(ds_row):
     #获取DS表的Item_group值
    global cal_delta_ds_item_group 
    cal_delta_ds_item_group = ds_row[('Total','Capabity')]
        
    if cal_delta_ds_item_group != "" and cal_delta_cp_item_group == cal_delta_ds_item_group :
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+5]
        iner_iter_df.apply(iner_Iter_From_Cal_Delta_Iter_In_Ds,axis=1)


def cal_delta_iter_in_cp(cp_row):
    global cal_delta_cp_row
    cal_delta_cp_row = cp_row
    #获取CP表的Item_group和siteid值
    global cal_delta_cp_item_group
    cal_delta_cp_item_group = cal_delta_cp_row['Item Group']
    siteid = cal_delta_cp_row['SITEID']
    global cal_delta_key 
    cal_delta_key = cal_delta_cp_item_group + "-" + siteid
    ds_df.apply(cal_Delta_Iter_In_Ds,axis=1)

def clear_Delta(row):
    if row[('Total','Capabity.1')] == 'Delta':
        row[('Current week','BOH')] = 0
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")

def clear_Loi(row):
    if row[('Total','Capabity.1')] == 'LOI':
        row[('Current week','BOH')] = 0
        print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")


#单独进程清除和计算delta的函数
def p_clear_and_cal_delta():
    #读取excel数据到内存
    read_excel()
    #先处理一下item_group的nan值
    handle_nan_item_group()
    #先清除Delta的值   
    clear_delta_start = time.time()
    ds_df.apply(clear_Delta,axis=1)
    clear_delta_end = time.time()
    print(f"进程-{os.getpid}清除Delta的值 time cost :",clear_delta_end - clear_delta_start)
    #开始计算Delta值
    cal_delta_start = time.time()
    cp_df.apply(cal_delta_iter_in_cp,axis=1)
    cal_delta_end = time.time()
    print(f"进程-{os.getpgid}计算Delta的值 time cost :",cal_delta_end - cal_delta_start)
    print(f"进程-{os.getpid}清除和计算Delta的值 time cost :",cal_delta_end - clear_delta_start)
    #释放数据
    delta_item_group_site_set.clear()
    #保存数据
    dict['ds_delta'] = ds_df

#单独进程清除和计算loi的函数
def p_clear_and_cal_loi():
    read_excel()
    clear_loi_start = time.time()
    ds_df.apply(clear_Loi,axis=1)
    clear_loi_end = time.time()
    print(f"进程-{os.getpid}清除Loi的值 time cost :",clear_loi_end - clear_loi_start)
    #开始计算loi
    cal_loi_start = time.time()
    cp_df.apply(Cal_Loi_Iter_In_Cp,axis=1)
    cal_loi_end = time.time()
    print(f"进程-{os.getpid}计算Loi的值 time cost :",cal_loi_end - cal_loi_start)
    print(f"进程-{os.getpid}清除和计算Loi的值 time cost :",cal_loi_end - clear_loi_start)
    #释放数据
    loi_item_group_site_set.clear()
    #保存数据
    dict['ds_loi'] = ds_df
    
######################################################Delta和Loi计算################################################


####################################################Demand和Supply计算##################################################

def clear_Demand_Iter_In_Ds(ds_row):
   
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
       
    if ds_total_capabity1 == "Demand":
        #遍历ds的日期列
        for k in range(5,len(ds_df.columns)):
            #获取DS表的日期值
            ds_month = ds_df.columns.get_level_values(0)[k]
            ds_datetime = ds_df.columns.get_level_values(1)[k]
            if clear_demand_cp_datetime == ds_datetime:
                ds_row[(f'{ds_month}',f'{ds_datetime}')] = 0
                print(f"清除{ds_row[('Total','Capabity')]}的{ds_total_capabity1}的日期{ds_datetime}的值")

def clear_demand():
    for i in range(54,len(cp_df.columns)): 
        #获取cp表的日期值
        global clear_demand_cp_datetime
        clear_demand_cp_datetime = cp_df.columns[i]
        ds_df.apply(clear_Demand_Iter_In_Ds,axis=1)

def clear_Supply_Iter_In_Ds(ds_row):
   
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
       
    if ds_total_capabity1 == "Supply":
        #遍历ds的日期列
        for k in range(5,len(ds_df.columns)):
            #获取DS表的日期值
            ds_month = ds_df.columns.get_level_values(0)[k]
            ds_datetime = ds_df.columns.get_level_values(1)[k]
            if clear_supply_cp_datetime == ds_datetime:
                ds_row[(f'{ds_month}',f'{ds_datetime}')] = 0
                print(f"清除{ds_row[('Total','Capabity')]}的{ds_total_capabity1}的日期{ds_datetime}的值")
    

def clear_supply():
    for i in range(54,len(cp_df.columns)): 
        #获取cp表的日期值
        global clear_supply_cp_datetime
        clear_supply_cp_datetime = cp_df.columns[i]
        ds_df.apply(clear_Supply_Iter_In_Ds,axis=1)


def cal_Demand_Iter_Cp(cp_row):
    cp_measure = cp_row['Measure']
    global cal_demand_cp_item_group 
    cal_demand_cp_item_group = cp_row['Item Group']
    global cal_demand_cp_row
    cal_demand_cp_row = cp_row
    if cp_measure == "Total Publish Demand":
        ds_df.apply(cal_Demand_Iter_Ds,axis=1)

def cal_demand():
    cp_df.apply(cal_Demand_Iter_Cp,axis=1)

def cal_demand_Inner_Iter_Ds(inner_iter_ds_row):
    if inner_iter_ds_row[('Total','Capabity.1')] == "Demand":
        for k in range(54,len(cp_df.columns)):
            for m in range(5,len(ds_df.columns)):
                #如果日期相同
                cp_datetime = cp_df.columns[k]
                ds_datetime = ds_df.columns.get_level_values(1)[m]
                ds_month = ds_df.columns.get_level_values(0)[m]
                if cp_datetime == ds_datetime:
                    inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cal_demand_cp_row[f'{cp_datetime}'],errors='coerce'))
                    print(f"{cal_demand_cp_item_group}的{inner_iter_ds_row[('Total','Capabity.1')]}的值={inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')]}")

def cal_Demand_Iter_Ds(ds_row):
    #如果cp和ds的item_group值相同
    ds_item_group = ds_row[('Total','Capabity')]
    if cal_demand_cp_item_group == ds_item_group:
        #从ds该行往下取4行作为一个slice进行处理
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+4]
        iner_iter_df.apply(cal_demand_Inner_Iter_Ds,axis=1)

def cal_Supply_Iter_Cp(cp_row):
    cp_measure = cp_row['Measure']
    global cal_supply_cp_item_group 
    cal_supply_cp_item_group = cp_row['Item Group']
    global cal_supply_cp_row
    cal_supply_cp_row = cp_row
    if cp_measure == "Total Commit" or cp_measure == "Total Risk Commit":
        ds_df.apply(cal_Supply_Iter_Ds,axis=1)

def cal_supply():
    cp_df.apply(cal_Supply_Iter_Cp,axis=1)

def cal_supply_Inner_Iter_Ds(inner_iter_ds_row):
    if inner_iter_ds_row[('Total','Capabity.1')] == "Supply":
        for k in range(54,len(cp_df.columns)):
            for m in range(5,len(ds_df.columns)):
                #如果日期相同
                cp_datetime = cp_df.columns[k]
                ds_datetime = ds_df.columns.get_level_values(1)[m]
                ds_month = ds_df.columns.get_level_values(0)[m]
                if cp_datetime == ds_datetime:
                    inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cal_supply_cp_row[f'{cp_datetime}'],errors='coerce'))
                    print(f"{cal_supply_cp_item_group}的{inner_iter_ds_row[('Total','Capabity.1')]}的值={inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')]}")
            
def cal_Supply_Iter_Ds(ds_row):
    #如果cp和ds的item_group值相同
    ds_item_group = ds_row[('Total','Capabity')]
    if cal_supply_cp_item_group == ds_item_group:
        #从ds该行往下取4行作为一个slice进行处理
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+4]
        iner_iter_df.apply(cal_supply_Inner_Iter_Ds,axis=1)

#单独进程清除和计算demand的函数
def p_clear_and_cal_demand():
    read_excel()
    #先清除Demand各个日期的值
    clear_demand_start = time.time()
    clear_demand()
    clear_demand_end = time.time()
    print(f"进程-{os.getpid}清空DS表Demand总共 time cost is :{clear_demand_end - clear_demand_start} seconds")
    #计算Demand各个日期的值
    cal_demand_start = time.time()
    cal_demand()
    cal_demand_end = time.time()
    print(f"进程-{os.getpid}计算DS表Demand值 time cost is :{cal_demand_end - cal_demand_start} seconds")
    #保存数据
    dict['ds_demand'] = ds_df

#单独进程清除和计算supply的函数
def p_clear_and_cal_supply():
    #读取excel数据到内存 
    read_excel()
    #先清除Supply各个日期的值
    clear_supply_start = time.time()
    clear_supply()
    clear_supply_end = time.time()
    print(f"进程-{os.getpid}清空DS表Supply总共 time cost is :{clear_supply_end - clear_supply_start} seconds")
    #计算Supply各个日期的值
    cal_supply_start = time.time()
    cal_supply()
    cal_supply_end = time.time()
    print(f"进程{os.getpid}计算DS表Supply的值 time cost is :{cal_supply_end - cal_supply_start} seconds")
    #保存数据
    dict['ds_supply'] = ds_df
    
    
######################################################Demand和Supply计算################################################ 

######################################################结果合并################################################ 

def iter_in_ds_df_delta(ds_df_supply,ds_df_delta_row):
    
    pass

def p_delta_merge_result(ds_df_delta,ds_df_supply):
    ds_df_delta.apply(iter_in_ds_df_delta,axis=1,args=ds_df_supply)

def p_loi_merge_result(ds_df_loi,ds_df_supply):
    pass

def p_demand_merge_result(ds_df_demand,ds_df_supply):
    pass

######################################################结果合并################################################ 


#先处理一下DS的item_group值，将Nan填充为真实的item_group值
real_ds_item_group = {'key':''}
def handle_nan_item_group_by_row(ds_df_row):
    cur_ds_item_group = ds_df_row[('Total','Capabity')]
    if type(cur_ds_item_group) == str and cur_ds_item_group != "" :
        real_ds_item_group['key'] = cur_ds_item_group
    else:
        ds_df_row[('Total','Capabity')] = real_ds_item_group['key']
        
def handle_nan_item_group():
    ds_df.apply(handle_nan_item_group_by_row,axis=1)
    

if __name__ == '__main__':

    print(f"主进程-{os.getpid()} is running...")
    
    cal_start = time.time()
    #起四个进程，同时计算delta、loi、demand和supply
    p_cal_delta = Process(target=p_clear_and_cal_delta,args=())
    p_cal_loi = Process(target=p_clear_and_cal_loi,args=())
    p_cal_demand = Process(target=p_clear_and_cal_demand,args=())
    p_cal_supply = Process(target=p_clear_and_cal_supply,args=())
    
    p_cal_delta.start()
    p_cal_loi.start()
    p_cal_demand.start()
    p_cal_supply.start()
    
    p_cal_delta.join()
    p_cal_loi.join()
    p_cal_demand.join()
    p_cal_supply.join()
    
    cal_end = time.time()
    print(f"ds_format python 脚本（使用多进程apply）内存计算总共 time cost is :{cal_end - cal_start} seconds") 
    
    #四个进程分别处理完后，拿到这四个进程的处理结果
    ds_df_delta = dict['ds_delta']
    ds_df_loi = dict['ds_loi']
    ds_df_demand = dict['ds_demand']
    ds_df_supply = dict['ds_supply']
    
    #起三个进程，分别将ds_df_delta、ds_df_loi和ds_df_demand合并到ds_df_supply
    merge_start = time.time()
    p_delta_merge = Process(target=p_delta_merge_result,args=(ds_df_delta,ds_df_supply))
    p_loi_merge = Process(target=p_loi_merge_result,args=(ds_df_loi,ds_df_supply))
    p_demand_merge = Process(target=p_demand_merge_result,args=(ds_df_demand,ds_df_supply))
    
    p_delta_merge.start()
    p_loi_merge.start()
    p_demand_merge.start()
    
    p_delta_merge.join()
    p_loi_merge.join()()
    p_demand_merge.join()
    merge_end = time.time()
    print(f"将内存计算结果进行合并time cost is :{merge_end - merge_start} seconds")
    
    #将内存计算结果保存到excel
    save_start = time.time()
    save_excel(ds_df_supply)
    save_end = time.time()
    print(f"将内存结果保存到excel总共 time cost is :{save_end - save_start} seconds")
    print(f"ds_format python 脚本（使用多进程apply）总共 time cost is :{save_end - cal_start} seconds")


   
    
    