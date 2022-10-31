"""
read data
csv、tsv、txt:pd.read_csv
excel: pd.read_excel
mysql: pd.read_sql
@author kingfish
"""
import pandas as pd

filepath = "./datas/ml-latest-small/ratings.csv"

ratings = pd.read_csv(filepath)

print("ratings 的前几行数据：\n")
print(ratings.head())
print("\n")

print("ratings 的行数和列数：\n")
print(ratings.shape)
print("\n")

print("ratings 的列：\n")
print(ratings.columns)
print("\n")
