"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas内置函数iterrows()来遍历DataFrame，但是是一个错误的使用示范
因为pandas的iterrows只能遍历和查询数据，并不能修改数据
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
for index,row in ds_df.iterrows():
    #print(row[('Total','Capabity.1')])
    if row[('Total','Capabity.1')] == 'Delta':
        row[('Current week','BOH')] = 0
    if row[('Total','Capabity.1')] == 'LOI':
        row[('Current week','BOH')] = 0
clear_delta_loi_end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

cal_delta_loi_start = time.time()
delta_item_group_site_set = set()
loi_item_group_site_set = set()

#根据CP和DS表的Item_group值做lookup，计算DS表的Delta和LOI值
for index_i,cp_row in cp_df.iterrows():
    
    #获取CP表的Item_group和siteid值
    cp_item_group = cp_row['Item Group']
    siteid = cp_row['SITEID']
    key = cp_item_group + "-" + siteid  
        
    for index_j,ds_row in ds_df.iterrows():
        
        #获取DS表的Item_group值
        ds_item_group = ds_row[('Total','Capabity')]
        
        if ds_item_group != "" and cp_item_group == ds_item_group :
           
            iner_iter_df = ds_df.loc[index_j:index_j+5]
           
            for index_k,ds_row_k in iner_iter_df.iterrows():
                
                ds_total_capabity1 = ds_row_k[('Total','Capabity.1')]
                
                #因为合并单元格的原因，item_group值可能为""或Nan，不管是何值都赋值为原item_group值
                ds_row_k[('Total','Capabity')] = ds_item_group
        
                #计算DS表的Delta值
                if ds_total_capabity1 == 'Delta':
                    #相同的item_group+siteid是否计算过
                    if (key in delta_item_group_site_set) == False:
                        delta_item_group_site_set.add(key)
                        ds_row_k[('Current week','BOH')] = handle_nan(pd.to_numeric(ds_row_k[('Current week','BOH')],errors='coerce')) + handle_nan(pd.to_numeric(cp_row['MRP (LOI)'],errors='coerce')) + handle_nan(pd.to_numeric(cp_row['MRP (OOI)'],errors='coerce'))                       
                        #print(f"item_group={ds_item_group}-Delta:{ ds_row_k[('Current week','BOH')]}")
                #计算DS表的LOI值
                if ds_total_capabity1 == 'LOI':
                    #相同的item_group+siteid是否计算过
                    if (key in loi_item_group_site_set) == False:
                        loi_item_group_site_set.add(key)
                        ds_row_k[('Current week','BOH')] = handle_nan(pd.to_numeric(ds_row_k[('Current week','BOH')],errors='coerce')) + handle_nan(pd.to_numeric(cp_row['MRP (LOI)'],errors='coerce'))
                        #print(f"item_group={ds_item_group}-LOI:{ ds_row_k[('Current week','BOH')]}")

#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")

clear_demand_supply_start = time.time()

#先清空Demand和Supply对应日期的值
for i in range(54,len(cp_df.columns)): 
    #获取cp表的日期值
    cp_datetime = cp_df.columns[i]
    
    for index_j,ds_row in ds_df.iterrows():
        
        #如果是DS表的Demand行或Supply行
        ds_total_capabity1 = ds_row[('Total','Capabity.1')]
       
        if ds_total_capabity1 == "Demand" or ds_total_capabity1 == "Supply":
            #遍历ds的日期列
            for k in range(5,len(ds_df.columns)):
                #获取DS表的日期值
                ds_month = ds_df.columns.get_level_values(0)[k]
                ds_datetime = ds_df.columns.get_level_values(1)[k]
                if cp_datetime == ds_datetime:
                    ds_row[(f'{ds_month}',f'{ds_datetime}')] = 0
                    #print(f"DS表第{j}行的日期{ds_datatime}清空")
                

clear_demand_supply_end = time.time()
print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end - clear_demand_supply_start} seconds")

cal_demand_supply_start = time.time()
#开始计算Demand和Supply的值
for index_j,cp_row in cp_df.iterrows():
    
    cp_measure = cp_row['Measure']
    cp_item_group = cp_row['Item Group']
    
    if cp_measure == "Total Publish Demand":
        
        for index_i,ds_row in ds_df.iterrows():
            #如果cp和ds的item_group值相同
            ds_item_group = ds_row[('Total','Capabity')]
            if cp_item_group == ds_item_group:
                #从ds该行往下取4行作为一个slice进行处理
                iner_iter_df = ds_df.loc[index_j:index_j+4]
                
                for iner_iter_index_q,iner_iter_df_row in iner_iter_df.iterrows():
                    
                    #因为合并单元格的原因，item_group值可能为""或Nan，不管是何值都赋值为本应该的原值item_group
                    iner_iter_df_row[('Total','Capabity')] = ds_item_group
                    
                    if iner_iter_df_row[('Total','Capabity.1')] == "Demand":
                        for k in range(54,len(cp_df.columns)):
                            for m in range(5,len(ds_df.columns)):
                                #如果日期相同
                                 cp_datetime = cp_df.columns[k]
                                 ds_datetime = ds_df.columns.get_level_values(1)[m]
                                 ds_month = ds_df.columns.get_level_values(0)[m]
                                 if cp_datetime == ds_datetime:
                                     iner_iter_df_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(iner_iter_df_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cp_row[f'{cp_datetime}'],errors='coerce'))
                                     
    if cp_measure == "Total Commit" or cp_measure == "Total Risk Commit":
        for index_i,ds_row in ds_df.iterrows():
            #如果cp和ds的item_group值相同
            ds_item_group = ds_row[('Total','Capabity')]
            if cp_item_group == ds_item_group:
                #从ds该行往下取4行作为一个slice进行处理
                iner_iter_df = ds_df.loc[index_j:index_j+4]
                
                for iner_iter_index_q,iner_iter_df_row in iner_iter_df.iterrows():
                    
                    #因为合并单元格的原因，item_group值可能为""或Nan，不管是何值都赋值为本应该的原值item_group
                    iner_iter_df_row[('Total','Capabity')] = ds_item_group
                    
                    if iner_iter_df_row[('Total','Capabity.1')] == "Supply":
                        for k in range(54,len(cp_df.columns)):
                            for m in range(5,len(ds_df.columns)):
                                #如果日期相同
                                 cp_datetime = cp_df.columns[k]
                                 ds_datetime = ds_df.columns.get_level_values(1)[m]
                                 ds_month = ds_df.columns.get_level_values(0)[m]
                                 if cp_datetime == ds_datetime:
                                     iner_iter_df_row[(f'{ds_month}',f'{ds_datetime}')] =  handle_nan(pd.to_numeric(iner_iter_df_row[(f'{ds_month}',f'{ds_datetime}')],errors='coerce')) + handle_nan(pd.to_numeric(cp_row[f'{cp_datetime}'],errors='coerce'))

cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用iterrow）内存计算总共 time cost is :{cal_demand_supply_end - clear_delta_loi_start} seconds")         

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
print(f"ds_format python 脚本（使用iterrow）总共 time cost is :{save_excel_end - read_excel_start} seconds")     
 