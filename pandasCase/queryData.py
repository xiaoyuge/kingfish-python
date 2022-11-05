"""@author kingfish
   用datafram查询数据
"""

import pandas as pd

data = pd.read_csv('datas/beijing_tianqi/beijing_tianqi_2018.csv');

#打印前几行数据
print('----------------------------打印前几行数据-----------------------------------')
print(data.head())
#设定日期列为索引，方便日期筛选
data.set_index('ymd',inplace=True)
#查看一下索引
print('----------------------------查看一下索引----------------------------------')
print(data.index)
#设置新的索引后，重新查看一下前几行
print('----------------------------设置新的索引后，重新查看一下前几行----------------------------------')
print(data.head())
#替换掉温度的后缀℃ 
data.loc[:,'bWendu'] = data['bWendu'].str.replace('℃','').astype('int32')
data.loc[:,'yWendu'] = data['yWendu'].str.replace('℃','').astype('int32')
#打印一下dataframe的数据类型
print('----------------------------打印一下dataframe的数据类型----------------------------------')
print(data.dtypes)
#打印前几行数据
print('----------------------------打印前几行数据----------------------------------')
print(data.head)
#查询某一天的最高温度
maxWendu = data.loc['2018-01-03',['bWendu']]
print('----------------------------查询某一天的最高温度----------------------------------')
print(maxWendu)
#查询某一天的最高和最低温度
maxAndMinWendu = data.loc['2018-01-03',['bWendu','yWendu']]
print('----------------------------查询某一天的最高和最低温度----------------------------------')
print(maxAndMinWendu)
#