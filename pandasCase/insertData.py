"""
@author kingfish
dataframe新增数据，三种方法：
1.直接赋值
2.apply方法
3.assign方法
4.分条件赋值方法
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
#处理一下数据，替换掉温度的后缀℃
data.loc[:,['bWendu']] = data['bWendu'].str.replace('℃','').astype('int32')
data.loc[:,['yWendu']] = data['yWendu'].str.replace('℃','').astype('int32')
print('----------------------------看一下替换掉温度后缀之后的数据----------------------------------')
print(data.loc[:,['bWendu','yWendu']])

"""
第一种方法：直接赋值

例子：
计算一下每天的温差，复制给新增的列
"""
#计算一下每天的温差，复制给新增的列wencha
data.loc[:,'wencha'] = data['bWendu'] - data['yWendu']
print('----------------------------看一下增加了温差列之后的数据----------------------------------')
print(data.loc[:,['bWendu','yWendu','wencha']])

"""
第二种方法：apply方法

例子：
添加一列温度类型
1.如果最高温度大于33度，则是高温；
2.如果温度低于-10度，则是低温；
3.否则则是常温
"""
def get_wendu_type(data):
    if data['bWendu'] > 33:
        return '高温'
    elif data['yWendu'] < -10:
        return '低温'
    else:
        return '常温'

data.loc[:,'wendu_type'] = data.apply(get_wendu_type,axis=1)
#打印出新增加的温度类型列数据
print('----------------------------打印出新增加的温度类型列数据----------------------------------')
print(data.loc[:,['bWendu','wendu_type']])    
print('----------------------------打印出高温数据----------------------------------')
print(data.loc[data['wendu_type']=='高温',:])
print('----------------------------打印出常温数据----------------------------------')
print(data.loc[data['wendu_type']=='常温',:])
print('----------------------------打印出温度类型的计数----------------------------------')
print(data['wendu_type'].value_counts())

"""
第三种方法：assign
注意assign不是操作原有的dataframe，而是会生成新的dataframe
assign可以同时操作多列

例子：
将温度从摄氏度转为华氏度
"""

#将温度从摄氏度转为华氏度
newData = data.assign(
    yWendu_huashi = lambda x: x['yWendu']*9/5 + 32,
    bWendu_huashi = lambda x: x['bWendu']*9/5 + 32
)
print('----------------------------打印出温度和华氏温度----------------------------------')
print(newData.loc[:,['bWendu','yWendu','bWendu_huashi','yWendu_huashi']])

"""
第四种方法：条件赋值

例子：
如果高温大于低温10度，则认为温差大
"""

#根据条件赋值：如果高温大于低温10度，则认为温差大
data.loc[data['bWendu'] - data['yWendu'] > 10,'wencha_type'] = '温差大'
data.loc[data['bWendu'] - data['yWendu'] <= 10,'wencha_type'] = '温差小'
print('----------------------------打印出高温、低温和温差大小----------------------------------')
print(data.loc[:,['bWendu','yWendu','wencha_type']])
print(data['wencha_type'].value_counts())

#上面的温差赋值，按照apply实现一遍
def get_wencha_type(x):
    if x['bWendu'] - x['yWendu'] > 10:
        return '温差大'
    if x['bWendu'] - x['yWendu'] <=10:
        return '温差小'
    
data.loc[:,'wencha_type'] = data.apply(get_wencha_type,axis=1)

print('----------------------------打印出高温、低温和温差大小----------------------------------')
print(data.loc[:,['bWendu','yWendu','wencha_type']])
print(data['wencha_type'].value_counts())