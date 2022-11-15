"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
"""

import pandas as pd
import xlwings as xw
import time

#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"

#把CP和DS两个sheet的数据分别读入pandas的dataframe
#cp_df = ds_format_workbook.sheets["CP"].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=float).value
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])


#先清空DS表的Delta和LOI列的值
start = time.time()
for i in range(0,len(ds_df)):
    print(ds_df.loc[i,('Total','Capabity.1')])
    if ds_df.loc[i,('Total','Capabity.1')] == "Delta":
        ds_df.loc[i,('Current week','BOH')] = 0
    if ds_df.loc[i,('Total','Capabity.1')] == "LOI":
        ds_df.loc[i,('Current week','BOH')] = 0
end = time.time()

print(f"清空DS表的Delta和LOI列的值 time cost is :{end-start} seconds")

start = time.time()
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
                        ds_df.loc[k,('Current week','BOH')] = pd.to_numeric(ds_df.loc[k,('Current week','BOH')]) + pd.to_numeric(cp_df.loc[i,'MRP (LOI)']) + pd.to_numeric(cp_df.loc[i,'MRP (OOI)'])
                       
                        print(f"item_group={ds_item_group}-Delta:{ds_df.loc[k,('Current week','BOH')] }")
                #计算DS表的LOI值
                if ds_total_capabity1 == 'LOI':
                    #相同的item_group+siteid是否计算过
                    if (key in loi_item_group_site_set) == False:
                        loi_item_group_site_set.add(key)
                        ds_df.loc[k,('Current week','BOH')] = pd.to_numeric(ds_df.loc[k,('Current week','BOH')]) + pd.to_numeric(cp_df.loc[i,'MRP (LOI)']) 
                        
                        print(f"item_group={ds_item_group}-LOI:{ds_df.loc[k,('Current week','BOH')] }")
                


#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()
            
end = time.time()

print(f"计算DS表的Delta和LOI列的值 time cost is :{end-start} seconds")