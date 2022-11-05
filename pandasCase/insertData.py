"""
@author kingfish
dataframe新增数据    
"""
import pandas as pd

#从csv文件读取数据
data = pd.read_csv('datas/beijing_tianqi/beijing_tianqi_2018.csv')

#看一下数据是否成功读取
print(data.head)
#探索一下数据
print('----------------------------探索一下数据----------------------------------')
print(data.loc[:,['bWendu']].dtypes)
print(data.loc[:,['bWendu']])
#替换掉温度的后缀℃
data.loc[:,['bWendu']] = data['bWendu'].str.replace('℃','').astype('int32')
data.loc[:,['yWendu']] = data['yWendu'].str.replace('℃','').astype('int32')
print('----------------------------看一下替换掉温度后缀之后的数据----------------------------------')
print(data.loc[:,['bWendu','yWendu']])
#计算一下每天的温差
data.loc[:,'wencha'] = data['bWendu'] - data['yWendu']
print('----------------------------看一下增加了温差列之后的数据----------------------------------')
print(data.loc[:,['bWendu','yWendu','wencha']])
