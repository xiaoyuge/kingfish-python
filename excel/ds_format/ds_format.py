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
#把CP和DS两个sheet的数据分别读入pandas的dataframe，对于formula会直接读取结果，导致会丢掉formula
cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])

#尝试用openpyxl读excel到dataframe，发现没有办法设置多级表头，但是可以读取的时候保留formula（data_only=False）参数
#ds_format_workbook = openpyxl.load_workbook(fpath,data_only=False)
#ds_wooksheet = ds_format_workbook['DS']
#ds_df =  pd.DataFrame(ds_wooksheet.values)

#使用xlwings来读取formula
app = xw.App(visible=False,add_book=False)
ds_format_workbook = app.books.open(fpath)
ds_worksheet = ds_format_workbook.sheets["DS"]

#保留excel中的formula
#找到DS中Total所在的行，Total之后的行都是formula
row = ds_df.loc[ds_df[('Total','Capabity')]=='Total ']
total_row_index = row.index.values[0]
#获取对应excel的行号(dataframe把两层表头当做索引，从数据行开始计数，而且从0开始计数。excel从表头就开始计数，而且从1开始计数)
excel_total_row_idx = int(total_row_index+2)
#获取excel最后一行的索引
excel_last_row_idx = ds_worksheet.used_range.rows.count
#保留按日期计算的各列的formula
I_col_formula = ds_worksheet.range(f'I3:I{excel_total_row_idx}').formula
N_col_formula = ds_worksheet.range(f'N3:N{excel_total_row_idx}').formula
T_col_formula = ds_worksheet.range(f'T3:T{excel_total_row_idx}').formula
U_col_formula = ds_worksheet.range(f'U3:U{excel_total_row_idx}').formula
Z_col_formula = ds_worksheet.range(f'Z3:Z{excel_total_row_idx}').formula
AE_col_formula = ds_worksheet.range(f'AE3:AE{excel_total_row_idx}').formula
AK_col_formula = ds_worksheet.range(f'AK3:AK{excel_total_row_idx}').formula
AL_col_formula = ds_worksheet.range(f'AL3:AL{excel_total_row_idx}').formula
#保留最后两列的formula
AN_col_formula = ds_worksheet.range(f'AN3:AN{excel_last_row_idx}').formula
AO_col_formula = ds_worksheet.range(f'AO3:AO{excel_last_row_idx}').formula
#保留Total行开始一直到末尾所有行的formula
total_to_last_formula = ds_worksheet.range(f'A{excel_total_row_idx+1}:AL{excel_last_row_idx}').formula

#下面两行代码是用xlwings读取所有数据到dataframe，对于有合并单元格的情况，只能这么写，否则会读不到完整数据，本脚本用不上，留在这里以备后用
#last_cell = ds_worksheet.used_range.last_cell
#ds_df = ds_worksheet.range((1,1),(last_cell.row,last_cell.column)).options(pd.DataFrame,index=False,header=2,dates=datetime.date).value

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
    ds_month = ds_df.columns.get_level_values(0)[i]
    #获取cp表的日期列
    cp_datetime_columns = cp_df.columns[53:]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_datetime_columns):
        ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(clear_demand_supply,axis=1,args=(ds_month,ds_datetime))

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
    ds_month = ds_df.columns.get_level_values(0)[i]
    #获取cp表的日期列
    cp_datetime_columns = cp_df.columns[53:]
    if type(ds_datetime) == str and ds_datetime != "" and (ds_datetime in cp_datetime_columns):
        ds_df[(f'{ds_month}',f'{ds_datetime}')] = ds_df.apply(cal_demand_supply_by_datetime,axis=1,args=(ds_month,ds_datetime))

cal_demand_supply_end = time.time()
print(f"计算DS表的Demand和Supply的值 time cost is :{cal_demand_supply_end - cal_demand_supply_start} seconds")
print(f"DS表的Demand和Supply的清空和计算总共 time cost is :{cal_demand_supply_end - clear_demand_supply_start} seconds")
print(f"ds_format python 脚本（使用apply）内存计算总共 time cost is :{cal_demand_supply_end - clear_delta_loi_start} seconds")   


save_excel_start = time.time()
#保存结果到excel                 
#直接把ds_df完整赋值给excel，会导致excel原有的公式被值覆盖
ds_worksheet.range("A1").expand().options(index=False).value = ds_df 
#用之前保留的formulas，重置公式
ds_worksheet.range(f'I3:I{excel_total_row_idx}').formula = I_col_formula
ds_worksheet.range(f'N3:N{excel_total_row_idx}').formula = N_col_formula
ds_worksheet.range(f'T3:T{excel_total_row_idx}').formula = T_col_formula
ds_worksheet.range(f'U3:U{excel_total_row_idx}').formula = U_col_formula
ds_worksheet.range(f'Z3:Z{excel_total_row_idx}').formula = Z_col_formula
ds_worksheet.range(f'AE3:AE{excel_total_row_idx}').formula = AE_col_formula
ds_worksheet.range(f'AK3:AK{excel_total_row_idx}').formula = AK_col_formula
ds_worksheet.range(f'AL3:AL{excel_total_row_idx}').formula = AL_col_formula
ds_worksheet.range(f'AN3:AN{excel_last_row_idx}').formula = AN_col_formula
ds_worksheet.range(f'AO3:AO{excel_last_row_idx}').formula = AO_col_formula
ds_worksheet.range(f'A{excel_total_row_idx+1}:AL{excel_last_row_idx}').formula = total_to_last_formula

ds_format_workbook.save()
ds_format_workbook.close()
app.quit()
save_excel_end = time.time()
print(f"保存结果到excel time cost is :{save_excel_end - save_excel_start} seconds") 
print(f"ds_format python 脚本（使用apply）总共 time cost is :{save_excel_end - read_excel_start} seconds") 
