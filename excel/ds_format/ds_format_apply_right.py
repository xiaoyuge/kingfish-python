"""
@author kingfish
这个代码来源于真实的需求，见/需求/需求文档.md
先切换工作目录到ds_format，然后执行该脚本
该实现使用Pandas的函数apply()来遍历DataFrame
PS：apply必须通过回调函数的返回值来修改datafram，在回调函数内部对dataframe修改是无效的
"""

import pandas as pd
import xlwings as xw
import time
import math
import openpyxl
import datetime

#要处理的文件路径
fpath = "data/DS_format.xlsm"
#fpath = "DS_format.xlsm"#打包exe的时候改成该路径

read_excel_start = time.time()
#把CP和DS两个sheet的数据分别读入pandas的dataframe
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1],dtype=str)
#找到DS中Total所在的行，只计算Total所在行之前的所有行，因为Total往后的行有公式，用df写入会覆盖公式
row = ds_df.loc[ds_df[('Total','Capabity')]=='Total ']
total_row_index = row.index.values[0]
ds_df = ds_df.loc[0:total_row_index -1 ]
read_excel_end = time.time()
print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")


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
        
ds_df[('Total','Capabity')] = ds_df.apply(handle_nan_item_group_by_row,axis=1)


clear_delta_loi_start = time.time()
#清空DS表的Delta和LOI列的值
def clear_Delta_Loi(row):
    item_group = row[('Total','Capabity')]
    capabity_1 = row[('Total','Capabity.1')]
    boh = row[('Current week','BOH')]
    
    if capabity_1 == 'Delta' and item_group.strip() != 'Total' and item_group.strip() != '1Gb  Eqv.':
        print(f"清除{item_group}的{capabity_1}的值")
        return 0
        
    if capabity_1 == 'LOI' and item_group.strip() != 'Total' and item_group.strip() != '1Gb  Eqv.':
        print(f"清除{item_group}的{capabity_1}的值")
        return 0
    
    return boh
    
ds_df[('Current week','BOH')] = ds_df.apply(clear_Delta_Loi,axis=1)

clear_delta_loi_end = time.time()
print(f"清空DS表的Delta和LOI列的值 time cost is :{clear_delta_loi_end - clear_delta_loi_start} seconds")

cal_delta_loi_start = time.time()
delta_item_group_site_set = set()
loi_item_group_site_set = set()

def handle_nan(data):
    if math.isnan(data):
        return 0
    return data

def Cal_Delta_Loi_Iter_In_Ds(ds_row):
    
    #获取DS表的Item_group值
    ds_item_group = ds_row[('Total','Capabity')]
    #获取DS表的Capabity.1的值，用于判断是delta还是loi
    ds_total_capabity1 = ds_row[('Total','Capabity.1')]
    #获取boh值，如果不是delta或loi，直接返回该值
    boh_val = ds_row[('Current week','BOH')]
    
    if ds_total_capabity1 == 'Delta' and ds_item_group.strip() != 'Total' and ds_item_group.strip() != '1Gb  Eqv.':
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
                print(f"item_group={ds_item_group}的Delta={ return_delta_val}")
        return return_delta_val
        
    if ds_total_capabity1 == 'LOI' and ds_item_group.strip() != 'Total' and ds_item_group.strip() != '1Gb  Eqv.':
        return_LOI_val = handle_nan(ds_row[('Current week','BOH')])
        #从cp_df获取item_group相等的一组数据
        selected_cp_df = cp_df.loc[cp_df['Item Group']==ds_item_group,:]
        for cp_df_index,cp_df_row in selected_cp_df.iterrows():
            key = cp_df_row['Item Group'] + '-' + cp_df_row['SITEID']
            if (key in delta_item_group_site_set) == False:
                LOI_value = handle_nan(ds_row[('Current week','BOH')])
                MRP_LOI_value = handle_nan(cp_df_row['MRP (LOI)'])
                return_LOI_val = return_LOI_val + pd.to_numeric(LOI_value,errors='coerce')+ pd.to_numeric(MRP_LOI_value,errors='coerce')
                print(f"item_group={ds_item_group}的LOI={ return_LOI_val}")
        return return_LOI_val
    
    return boh_val

#计算Dela和LOI的值
ds_df[('Current week','BOH')] = ds_df.apply(Cal_Delta_Loi_Iter_In_Ds,axis=1)

#释放数据
delta_item_group_site_set.clear()
loi_item_group_site_set.clear()

cal_delta_loi_end = time.time()
print(f"计算DS表的Delta和LOI列的值 time cost is :{cal_delta_loi_end - cal_delta_loi_start} seconds")

clear_demand_supply_start = time.time()

def clear_demand_supply(ds_row,ds_month,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    if (Capabity_1 == 'Demand' or Capabity_1 == 'Supply') and (ds_item_group.strip() != 'Total' and ds_item_group.strip() != '1Gb  Eqv.'):
        print(f'清空{ds_item_group}的{Capabity_1}的日期{ds_month}:{ds_datetime}的值')
        return 0
    else:
        return ds_row[(f'{ds_month}',f'{ds_datetime}')]

#清除DS表Demand和Supply各个日期的值
#根据DS和CP相同的日期，计算Demand和Supply值
for i in range(4,len(ds_df.columns)):
    ds_datetime = ds_df.columns.get_level_values(1)[i]
    iter_ds_month = ds_df.columns.get_level_values(0)[i]
    #获取cp表的日期列
    cp_datetime_columns = cp_df.columns[53:]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_datetime_columns):
        ds_df[(f'{iter_ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_demand_supply,axis=1,args=(iter_ds_month,ds_datetime))

clear_demand_supply_end = time.time()
print(f"清空DS表的Demand和Supply的值 time cost is :{clear_demand_supply_end - clear_demand_supply_start} seconds")    

cal_demand_supply_start = time.time()

def cal_demand_supply_by_datetime(ds_row,ds_month,ds_datetime):
    ds_item_group = ds_row[('Total','Capabity')]
    Capabity_1 = ds_row[('Total','Capabity.1')]
    
    if Capabity_1 == 'Demand' and ds_item_group.strip() != 'Total' and ds_item_group.strip() != '1Gb  Eqv.':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & (cp_df['Measure']=='Total Publish Demand'),:]
        return_damand_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_damand_val = return_damand_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_month}:{ds_datetime}的值={return_damand_val}")
        return return_damand_val
    
    if Capabity_1 == 'Supply' and ds_item_group.strip() != 'Total' and ds_item_group.strip() != '1Gb  Eqv.':
        selected_cp_df = cp_df.loc[(cp_df['Item Group']==ds_item_group) & ((cp_df['Measure']=='Total Commit') | (cp_df['Measure']=='Total Risk Commit')),:]
        return_supply_val = 0
        for index_cp_df,cp_df_row in selected_cp_df.iterrows():
            return_supply_val = return_supply_val + cp_df_row[ds_datetime]
        print(f"item_group={ds_item_group}的{Capabity_1}的日期为{ds_month}:{ds_datetime}的值={return_supply_val}")
        return return_supply_val
    
    return ds_row[(f'{ds_month}',f'{ds_datetime}')]

#根据DS和CP相同的日期，计算Demand和Supply值
for i in range(4,len(ds_df.columns)):
    ds_datetime = ds_df.columns.get_level_values(1)[i]
    iter_ds_month = ds_df.columns.get_level_values(0)[i]
    #获取cp表的日期列
    cp_datetime_columns = cp_df.columns[53:]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_datetime_columns):
        ds_df[(f'{iter_ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_demand_supply_by_datetime,axis=1,args=(iter_ds_month,ds_datetime))

cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用apply）内存计算总共 time cost is :{cal_demand_supply_end - clear_delta_loi_start} seconds")   


save_excel_start = time.time()
#保存结果到excel       
app = xw.App(visible=False,add_book=False)

ds_format_workbook = app.books.open(fpath)
ds_worksheet = ds_format_workbook.sheets["DS"]

"""该块代码尝试遍历dataframe然后按单元格写入对应的值，但是用xlwings操作单元格频繁写入非常慢（40分钟），不可接受，放弃
但保留该块代码以供瞻仰
#根据ds_df来写excel，只写该写的单元格
for row_idx,row in ds_df.iterrows():
    total_capabity_val = row[('Total','Capabity')].strip()
    total_capabity1_val = row[('Total','Capabity.1')].strip()
    #Total和1Gb  Eqv.所在的行不写
    if total_capabity_val!= 'Total' and total_capabity_val != '1Gb  Eqv.':
        #给Delta和LOI赋值
        if total_capabity1_val == 'LOI' or total_capabity1_val == 'Delta':
            ds_worksheet.range((row_idx + 3 ,3)).value = row[('Current week','BOH')]
            print(f"ds_sheet的第{row_idx + 3}行第3列被设置为{row[('Current week','BOH')]}") 
        #给Demand和Supply赋值
        if total_capabity1_val == 'Demand' or total_capabity1_val == 'Supply':
            cp_datetime_columns = cp_df.columns[53:]
            for col_idx in range(4,len(ds_df.columns)):
                ds_datetime = ds_df.columns.get_level_values(1)[col_idx]
                ds_month = ds_df.columns.get_level_values(0)[col_idx]
                if type(ds_datetime) == str and ds_datetime != 'TTL' and ds_datetime != 'Total' and (ds_datetime in cp_datetime_columns):
                    ds_worksheet.range((row_idx + 3,col_idx + 1)).value = row[(f'{ds_month}',f'{ds_datetime}')]
                    print(f"ds_sheet的第{row_idx + 3}行第{col_idx + 1}列被设置为{row[(f'{ds_month}',f'{ds_datetime}')]}") 
                elif type(ds_datetime) == datetime.datetime and (ds_datetime in cp_datetime_columns):
                    ds_worksheet.range((row_idx + 3,col_idx + 1)).value = row[(f'{ds_month}',ds_datetime)]     
                    print(f"ds_sheet的第{row_idx + 3}行第{col_idx + 1}列被设置为{row[(f'{ds_month}',ds_datetime)]}")             
"""   

"""这段代码打算按excel的区域，来给excel批量赋值，结果败在了日期类型的表头上
last_row_idx = int(total_row_index+1)
#赋值Delta和LOI
ds_worksheet.range((3,3),(last_row_idx,3)).value = ds_df[('Current week','BOH')].to_list()

#赋值Demand和Supply
for col_idx in range(4,len(ds_df.columns)):
    ds_datetime = ds_df.columns.get_level_values(1)[col_idx]
    iter_ds_month = ds_df.columns.get_level_values(0)[col_idx]
    #找到日期列
    if type(ds_datetime) == str and (ds_datetime == 'TTL' or ds_datetime == 'Total'):
        continue
    #找到后获取日期列的列索引值作为起始索引值
    start_col_idx = col_idx
    #start_ds_datetime = ds_df.columns.get_level_values(1)[start_col_idx]
    #start_ds_month = ds_df.columns.get_level_values(0)[start_col_idx]
    df_loc_col_str = '['
    #df_loc_col_str = df_loc_col_str + f"('{start_ds_month}','{start_ds_datetime}'),"
    #从起始日期列，往后找到最后一个不是TTL或Total的日期列，作为末尾日期列，确定范围
    for iter_col_idx in range(start_col_idx,len(ds_df.columns)):
        iter_ds_datetime = ds_df.columns.get_level_values(1)[iter_col_idx]
        iter_ds_month = ds_df.columns.get_level_values(0)[iter_col_idx]
        if type(iter_ds_datetime) == str and (iter_ds_datetime == 'TTL' or iter_ds_datetime == 'Total'):
            end_col_idx = iter_col_idx -1 
            end_ds_datetime = ds_df.columns.get_level_values(1)[end_col_idx]
            end_ds_month = ds_df.columns.get_level_values(0)[end_col_idx]
            df_loc_col_str = df_loc_col_str + ']'
            #给excel赋值
            ds_worksheet.range((3,start_col_idx+1),(last_row_idx,end_col_idx+1)).value = ds_df.loc[0:last_row_idx,f"{df_loc_col_str}"]
            #从末尾列往后循环
            col_idx = end_col_idx + 1
        else:
            if type(iter_ds_datetime) == str:
                df_loc_col_str = df_loc_col_str + f"('{iter_ds_month}','{iter_ds_datetime}'),"  
            elif type(iter_ds_datetime) == datetime.datetime :
                df_loc_col_str = df_loc_col_str + f"('{iter_ds_month}',{iter_ds_datetime})," 
"""

#直接把ds_df完整赋值给excel，会导致excel原有的公式被值覆盖，因为之前的代码只读取了total之前的行，所以total以及total往后的行
#的公式不会背覆盖，但是日期列中的total和ttl还是会被覆盖，没有完美解决
ds_worksheet.range("A1").expand().options(index=False).value = ds_df 

ds_format_workbook.save()
ds_format_workbook.close()
app.quit()
save_excel_end = time.time()
print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 
print(f"ds_format python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
