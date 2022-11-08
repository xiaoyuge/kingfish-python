    
"""
@author kingfish
熟悉Series
"""
    
import pandas as pd
    
data = {
    'state':['Ohio','Ohio','Ohio','Nevada','Nevada'],
    'year':[2000,2001,2002,2002,2006],
    'pop':[1.5,1.7,1.6,2.4,2.9]
}
    
df = pd.DataFrame(data)
    
#打印dataframe  
print('----------------------------打印dataframe的列-----------------------------------')
print(type(df.columns))
print(df.columns)
print('----------------------------打印dataframe的state列-----------------------------------')
print(type(df['state']))
print(df['state'])
print('----------------------------打印dataframe的state和pop列-----------------------------------')
print(type(df[['state','pop']]))
print(df[['state','pop']])
print('----------------------------打印dataframe的第0行-----------------------------------')
print(type(df.loc[0]))
print(df.loc[0])
print('----------------------------打印dataframe的第1-2行-----------------------------------')
print(type(df.loc[1:2]))
print(df.loc[1:2])