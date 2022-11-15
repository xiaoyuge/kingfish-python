"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas内置函数iterrows()来遍历DataFrame
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

start = time.time()
#先清空DS表的Delta和LOI列的值
for index,row in ds_df.iterrows():
    print(row[('Total','Capabity.1')])
    if row[('Total','Capabity.1')] == 'Delta':
        row[('Current week','BOH')] = 0
    if row[('Total','Capabity.1')] == 'LOI':
        row[('Current week','BOH')] = 0
end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{end-start} seconds")


start = time.time()
delta_item_group_site_set = set()
loi_item_group_site_set = set()

#根据CP和DS表的Item_group值做lookup，计算DS表的Delta值
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
        
                #计算DS表的Delta值
                if ds_total_capabity1 == 'Delta':
                    #相同的item_group+siteid是否计算过
                    if (key in delta_item_group_site_set) == False:
                        delta_item_group_site_set.add(key)
                        ds_row_k[('Current week','BOH')] = pd.to_numeric(ds_row_k[('Current week','BOH')]) + pd.to_numeric(cp_row['MRP (LOI)']) + pd.to_numeric(cp_row['MRP (OOI)'])                        
                        print(f"item_group={ds_item_group}-Delta:{ ds_row_k[('Current week','BOH')]}")
                #计算DS表的LOI值
                if ds_total_capabity1 == 'LOI':
                    #相同的item_group+siteid是否计算过
                    if (key in loi_item_group_site_set) == False:
                        loi_item_group_site_set.add(key)
                        ds_row_k[('Current week','BOH')] = pd.to_numeric(ds_row_k[('Current week','BOH')],errors='coerce') + pd.to_numeric(cp_row['MRP (LOI)'],errors='coerce') 
                        print(f"item_group={ds_item_group}-LOI:{ ds_row_k[('Current week','BOH')]}")
                


#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{end-start} seconds")
            
