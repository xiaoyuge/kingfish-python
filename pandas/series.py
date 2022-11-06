"""
@author kingfish
熟悉Series
"""

import pandas as pd

s1 = pd.Series([1,'a',5,2,7])

#s1的值
print('s1的值:\n')
print(s1)

#s1的index
print('s1的index:\n')
print(s1.index)

#s1的values
print('s1的values:\n')
print(s1.values)

#自己创建一个series
s2 = pd.Series([1,'2',5,2,7],index=['d','b','a','c','e'])

#s2的值
print('s2的值:\n')
print(s2)

#s2的index
print('s2的index:\n')
print(s2.index)

#s2的values
print('s2的values:\n')
print(s2.values)

#使用python字典创建Series
sdata = {'Ohio':35000,'Texas':72000,'Oregon':16000,'Utah':5000}

s3 = pd.Series(sdata)

#s3的值
print('s3的值:\n')
print(s3)

#s3的index
print('s3的index:\n')
print(s3.index)

#s3的values
print('s3的values:\n')
print(s3.values)

#获取Series的值，可以用类似字典获取数据的方法

#获取S3的Texas的值
Texas = s3['Texas']

print('获取S3的Texas的类型和值:\n')
print(type(Texas))
print(Texas)

#获取S3的Texas和Utah值
TexasAndUtah = s3[['Texas','Utah']]

print('获取S3的Texas和Utah值:\n')
print(type(TexasAndUtah))
print(TexasAndUtah)
