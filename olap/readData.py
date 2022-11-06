"""
read data
csv、tsv、txt:pd.read_csv
excel: pd.read_excel
mysql: pd.read_sql
@author kingfish
"""

import pandas as pd

"""
读取csv文件
"""

#获取csv文件
filepath = "datas/ml-latest-small/ratings.csv"

#读取csv文件
ratings = pd.read_csv(filepath)

#查看ratings的前几行数据
print("ratings 的前几行数据：\n")
print(ratings.head())
print("\n")

#查看ratings的行数和列数
print("ratings 的行数和列数：\n")
print(ratings.shape)
print("\n")

#查看ratings的列名
print("ratings的列：\n")
print(ratings.columns)
print("\n")

#查看ratings的索引列
print("ratings的索引列:")
print(ratings.index)

#查看ratings每列的数据类型
print("ratings每列的数据类型:")
print(ratings.dtypes)

print("--------------------------------------------------")

"""
读取txt文件
"""
filepath = "~/kingfish-python/kingfish-python/datas/crazyant/access_pvuv.txt"

pvuv = pd.read_csv(filepath,sep="\t",header=None,names=['pdate','uv','pv'])

print(pvuv)

print("--------------------------------------------------")

"""
读取excel文件
"""

filepath = "~/kingfish-python/kingfish-python/datas/crazyant/access_pvuv.xlsx"

pvuv = pd.read_excel(filepath)

print(pvuv)
