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
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
    if row[('Total','Capabity.1')] == 'LOI':
        row[('Current week','BOH')] = 0
        #print(f"清除{row[('Total','Capabity')]}的{row[('Total','Capabity.1')]}的值")
    
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

def iner_Iter_From_Cal_Delta_Loi_Iter_In_Ds(ds_row_k):
                  
    ds_total_capabity1 = ds_row_k[('Total','Capabity.1')]
        
    #计算DS表的Delta值
    if ds_total_capabity1 == 'Delta':
    #相同的item_group+siteid是否计算过
        if (key in delta_item_group_site_set) == False:
            delta_item_group_site_set.add(key)
            delta_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan((cal_delta_loi_cp_row['MRP (LOI)']))
            MRP_OOI_value = handle_nan(cal_delta_loi_cp_row['MRP (OOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(delta_value,errors='coerce') + pd.to_numeric(MRP_LOI_value,errors='coerce') + pd.to_numeric(MRP_OOI_value,errors='coerce')                        
            #print(f"item_group={cal_delta_loi_ds_item_group}的Delta={ ds_row_k[('Current week','BOH')]}")
    #计算DS表的LOI值
    if ds_total_capabity1 == 'LOI':
        #相同的item_group+siteid是否计算过
        if (key in loi_item_group_site_set) == False:
            loi_item_group_site_set.add(key)
            LOI_value = handle_nan(ds_row_k[('Current week','BOH')])
            MRP_LOI_value = handle_nan(cal_delta_loi_cp_row['MRP (LOI)'])
            ds_row_k[('Current week','BOH')] = pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
            #print(f"item_group={cal_delta_loi_ds_item_group}的LOI={ ds_row_k[('Current week','BOH')]}")

def Cal_Delta_Loi_Iter_In_Ds(ds_row):
    
      #获取DS表的Item_group值
        global cal_delta_loi_ds_item_group 
        cal_delta_loi_ds_item_group = ds_row[('Total','Capabity')]
        
        if cal_delta_loi_ds_item_group != "" and cp_item_group == cal_delta_loi_ds_item_group :
            index_j = ds_row.name
            iner_iter_df = ds_df.loc[index_j:index_j+5]
            iner_iter_df.apply(iner_Iter_From_Cal_Delta_Loi_Iter_In_Ds,axis=1)


def Cal_Delta_Loi_Iter_In_Cp(data):
    global cal_delta_loi_cp_row
    cal_delta_loi_cp_row = data
    #获取CP表的Item_group和siteid值
    global cp_item_group
    cp_item_group = cal_delta_loi_cp_row['Item Group']
    siteid = cal_delta_loi_cp_row['SITEID']
    global key 
    key = cp_item_group + "-" + siteid
    ds_df.apply(Cal_Delta_Loi_Iter_In_Ds,axis=1)
    
#开始计算Delta和LOI值
cp_df.apply(Cal_Delta_Loi_Iter_In_Cp,axis=1)

#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")

clear_demand_supply_start = time.time()

def clear_Demand_Supply_Iter_In_Ds(ds_row):
     #如果是DS表的Demand行或Supply行
        ds_total_capabity1 = ds_row[('Total','Capabity.1')]
       
        if ds_total_capabity1 == "Demand" or ds_total_capabity1 == "Supply":
            #遍历ds的日期列
            for k in range(5,len(ds_df.columns)):
                #获取DS表的日期值
                ds_month = ds_df.columns.get_level_values(0)[k]
                ds_datetime = ds_df.columns.get_level_values(1)[k]
                if clear_demand_supply_cp_datetime == ds_datetime:
                    ds_row[(f'{ds_month}',f'{ds_datetime}')] = 0
                    #print(f"清除{ds_row[('Total','Capabity')]}的{ds_total_capabity1}的日期{ds_datetime}的值")
    
#清除DS表Demand和Supply各个日期的值
for i in range(54,len(cp_df.columns)): 
    #获取cp表的日期值
    global clear_demand_supply_cp_datetime
    clear_demand_supply_cp_datetime = cp_df.columns[i]
    
    ds_df.apply(clear_Demand_Supply_Iter_In_Ds,axis=1)

clear_demand_supply_end = time.time()
print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end - clear_demand_supply_start} seconds")    

cal_demand_supply_start = time.time()

def cal_damand_Inner_Iter_Ds(inner_iter_ds_row):
    if inner_iter_ds_row[('Total','Capabity.1')] == "Demand":
        for k in range(54,len(cp_df.columns)):
            for m in range(5,len(ds_df.columns)):
                #如果日期相同
                cp_datetime = cp_df.columns[k]
                ds_datetime = ds_df.columns.get_level_values(1)[m]
                ds_month = ds_df.columns.get_level_values(0)[m]
                if cp_datetime == ds_datetime:
                    inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cal_demand_supply_cp_row[f'{cp_datetime}'],errors='coerce'))
                    #print(f"{cal_demand_supply_cp_item_group}的{inner_iter_ds_row[('Total','Capabity.1')]}的值={inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')]}")

#开始计算Demand和Supply的值
def cal_Demand_Iter_Ds(ds_row):
    #如果cp和ds的item_group值相同
    ds_item_group = ds_row[('Total','Capabity')]
    if cal_demand_supply_cp_item_group == ds_item_group:
        #从ds该行往下取4行作为一个slice进行处理
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+4]
        iner_iter_df.apply(cal_damand_Inner_Iter_Ds,axis=1)

def cal_supply_Inner_Iter_Ds(inner_iter_ds_row):
    if inner_iter_ds_row[('Total','Capabity.1')] == "Supply":
        for k in range(54,len(cp_df.columns)):
            for m in range(5,len(ds_df.columns)):
                #如果日期相同
                cp_datetime = cp_df.columns[k]
                ds_datetime = ds_df.columns.get_level_values(1)[m]
                ds_month = ds_df.columns.get_level_values(0)[m]
                if cp_datetime == ds_datetime:
                    inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cal_demand_supply_cp_row[f'{cp_datetime}'],errors='coerce'))
                    #print(f"{cal_demand_supply_cp_item_group}的{inner_iter_ds_row[('Total','Capabity.1')]}的值={inner_iter_ds_row[(f'{ds_month}',f'{ds_datetime}')]}")
            
def cal_Supply_Iter_Ds(ds_row):
    #如果cp和ds的item_group值相同
    ds_item_group = ds_row[('Total','Capabity')]
    if cal_demand_supply_cp_item_group == ds_item_group:
        #从ds该行往下取4行作为一个slice进行处理
        index_j = ds_row.name
        iner_iter_df = ds_df.loc[index_j:index_j+4]
        iner_iter_df.apply(cal_supply_Inner_Iter_Ds,axis=1)

def cal_Demand_Supply_Iter_Cp(cp_row):
    cp_measure = cp_row['Measure']
    global cal_demand_supply_cp_item_group 
    cal_demand_supply_cp_item_group = cp_row['Item Group']
    global cal_demand_supply_cp_row
    cal_demand_supply_cp_row = cp_row
    
    if cp_measure == "Total Publish Demand":
        ds_df.apply(cal_Demand_Iter_Ds,axis=1)
        
    if cp_measure == "Total Commit" or cp_measure == "Total Risk Commit":
        ds_df.apply(cal_Supply_Iter_Ds,axis=1)


cp_df.apply(cal_Demand_Supply_Iter_Cp,axis=1)

cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用apply）内存计算总共 time cost is :{cal_demand_supply_end - clear_delta_loi_start} seconds")   

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
print(f"ds_format python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
