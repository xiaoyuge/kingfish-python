"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用标准循环来遍历pandas的DataFrame
"""

import pandas as pd
import xlwings as xw
import time

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"
read_excel_start = time.time()
#把CP和DS两个sheet的数据分别读入pandas的dataframe
#cp_df = ds_format_workbook.sheets["CP"].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=float).value
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
read_excel_end = time.time()
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")

clear_start = time.time()
#先清空DS表的Delta和LOI列的值
for i in range(0,len(ds_df)):
    if ds_df.loc[i,('Total','Capabity.1')] == "Delta":
        ds_df.loc[i,('Current week','BOH')] = 0
    if ds_df.loc[i,('Total','Capabity.1')] == "LOI":
        ds_df.loc[i,('Current week','BOH')] = 0
clear_end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_end-clear_start} seconds")

#开始delta和loi的计算
cal_delta_loi_start = time.time()

delta_item_group_site_set = set()
loi_item_group_site_set = set()

#根据CP和DS表的Item_group值做lookup，计算DS表的Delta值
for i in range(0,len(cp_df)):
    
    #获取CP表的Item_group和siteid值
    cp_item_group = cp_df.loc[i,'Item Group']
    siteid = cp_df.loc[i,'SITEID']
    key = cp_item_group + "-" + siteid  
        
    for j in range(0,len(ds_df)):
        
        #获取DS表的Item_group值
        ds_item_group = ds_df.loc[j,('Total','Capabity')]
        
        if ds_item_group != "" and cp_item_group == ds_item_group :
            for k in range(j,j+5):
                ds_total_capabity1 = ds_df.loc[k,('Total','Capabity.1')]
                #计算DS表的Delta值
                if ds_total_capabity1 == 'Delta':
                    #相同的item_group+siteid是否计算过
                    if (key in delta_item_group_site_set) == False:
                        delta_item_group_site_set.add(key)
                        ds_df.loc[k,('Current week','BOH')] = float(ds_df.loc[k,('Current week','BOH')]) + float(cp_df.loc[i,'MRP (LOI)']) + float(cp_df.loc[i,'MRP (OOI)'])
                        #print(f"item_group={ds_item_group}-Delta")
                #计算DS表的LOI值
                if ds_total_capabity1 == 'LOI':
                    #相同的item_group+siteid是否计算过
                    if (key in loi_item_group_site_set) == False:
                        loi_item_group_site_set.add(key)
                        ds_df.loc[k,('Current week','BOH')] = float(ds_df.loc[k,('Current week','BOH')]) + float(cp_df.loc[i,'MRP (LOI)']) 
                        #print(f"item_group={ds_item_group}-LOI")
                


#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI的值 time cost is :{cal_delta_loi_end-cal_delta_loi_start} seconds")
print(f"DS表的Delta和LOI的清空和计算总共 time cost is :{cal_delta_loi_end-clear_start} seconds")

clear_demand_supply_start = time.time()

#先清空Demand和Supply对应日期的值
for i in range(54,len(cp_df.columns)):
    #获取cp表的日期值
    cp_datatime = cp_df.columns[i]
    
    for j in range(3,len(ds_df)):
        #如果是DS表的Demand行或Supply行
        ds_total_capabity1 = ds_df.loc[j,('Total','Capabity.1')]
        if ds_total_capabity1 == "Demand" or ds_total_capabity1 == "Supply":
            #遍历ds的日期列
            for k in range(5,len(ds_df.columns)):
                #获取DS表的日期值
                ds_month = ds_df.columns.get_level_values(0)[k]
                ds_datatime = ds_df.columns.get_level_values(1)[k]
                if cp_datatime == ds_datatime:
                    ds_df.loc[j,(f'{ds_month}',f'{ds_datatime}')] = 0
                    #print(f"DS表第{j}行的日期{ds_datatime}清空")
                

clear_demand_supply_end = time.time()
print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end-clear_demand_supply_start} seconds")


cal_demand_supply_start = time.time()
#开始按日期计算Demand和Supply的值
for j in range(len(cp_df)):
    
    cp_measure = cp_df.loc[j,'Measure']
    cp_item_group = cp_df.loc[j,'Item Group']
    
    if cp_measure == "Total Publish Demand":
        
        for i in range(len(ds_df)):
            #如果cp和ds的item_group值相同
            if cp_item_group == ds_df.loc[i,('Total','Capabity')]:
                
                for q in range(i,i+4):
                    if ds_df.loc[q,('Total','Capabity.1')] == "Demand":
                        
                        for k in range(54,len(cp_df.columns)):
                            for m in range(5,len(ds_df.columns)):
                                #如果日期相同
                                 cp_datatime = cp_df.columns[k]
                                 ds_datatime = ds_df.columns.get_level_values(1)[m]
                                 ds_month = ds_df.columns.get_level_values(0)[m]
                                 if cp_datatime == ds_datatime:
                                     ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')] =  ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')] + cp_df.loc[j,f'{cp_datatime}']
                                     #print(f"{cp_item_group}-Demard:{ ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')]}")
    
    if cp_measure == "Total Commit" or cp_measure == "Total Risk Commit":
        for i in range(len(ds_df)):
            if cp_item_group == ds_df.loc[i,('Total','Capabity')]: 
                for q in range(i,i+4):
                    if ds_df.loc[q,('Total','Capabity.1')] == "Supply":
                         for k in range(54,len(cp_df.columns)):
                            for m in range(5,len(ds_df.columns)):
                                #如果日期相同
                                 cp_datatime = cp_df.columns[k]
                                 ds_datatime = ds_df.columns.get_level_values(1)[m]
                                 ds_month = ds_df.columns.get_level_values(0)[m]
                                 if cp_datatime == ds_datatime:
                                     ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')] =  ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')] + cp_df.loc[j,f'{cp_datatime}']    
                                     #print(f"{cp_item_group}-Supply:{ ds_df.loc[q,(f'{ds_month}',f'{ds_datatime}')]}")


cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end-cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end-clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用普通循环）内存计算总共 time cost is :{cal_demand_supply_end-clear_start} seconds")

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
print(f"ds_format python 脚本（使用普通循环）总共 time cost is :{save_excel_end - read_excel_start} seconds")       
            
            
