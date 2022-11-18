"""
@author kingfish
这个代码来源于真实的需求，见/data/joyce/需求文档.md
该实现使用Pandas的函数apply()来遍历DataFrame，并且开启多线程来加速计算
但是该场景是一个CPU密集型场景，python多线程因为GIL的原因，并不能利用到多核加速
"""

import pandas as pd
import xlwings as xw
import time
import math
from threading import Thread


#要处理的文件路径
fpath = "datas/joyce/DS_format_bak.xlsm"

def read_excel():
    #要处理的文件路径
    read_excel_start = time.time()
    #把CP和DS两个sheet的数据分别读入pandas的dataframe
    #cp_df = ds_format_workbook.sheets["CP"].range("A1").options(pd.DataFrame,expand='table',index=False,numbers=float).value
    global cp_df 
    cp_df = pd.read_excel(fpath,sheet_name="CP",header=[0])
    global ds_df 
    ds_df = pd.read_excel(fpath,sheet_name="DS",header=[0,1])
    read_excel_end = time.time()
    print(f"读取excel文件 time cost is :{read_excel_end - read_excel_start} seconds")

    
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


def p_clear_and_cal_delta():
    
    pass

def p_clear_and_cal_loi():
    pass

def p_clear_and_cal_demand():
    pass

def p_clear_and_cal_supply():
    pass


if __name__ == "__main__":
    
    app_start = time.time()
    #读取excel数据到内存
    read_excel()
    
    #开启四个线程开始计算
    cal_start = time.time()
    t_cal_delta = Thread(target=p_clear_and_cal_delta,args=())
    t_cal_delta.start()
    
    t_cal_loi = Thread(target=p_clear_and_cal_loi,args=())
    t_cal_loi.start()
    
    t_cal_demand = Thread(target=p_clear_and_cal_demand,args=())
    t_cal_demand.start()
    
    t_cal_supply = Thread(target=p_clear_and_cal_supply,args=())
    t_cal_supply.start()
    
    t_cal_delta.join()
    t_cal_loi.join()
    t_cal_demand.join()
    t_cal_supply.join()
    
    cal_end = time.time()
    print(f"ds_format python 脚本（使用多线程apply）内存计算总共 time cost is :{cal_end - cal_start} seconds") 
    
    #内存数据写入excel
    save_excel()
    
    app_end = time.time()
    print(f"ds_format python 脚本（使用多进程apply）总共 time cost is :{app_end - app_start} seconds")