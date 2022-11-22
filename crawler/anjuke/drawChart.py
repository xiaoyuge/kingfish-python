"""
读取excel数据，分析数据并生成图表
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar
    
def cal_square_district(row):
    if row['面积'] <= 60:
        return '[0,60]'
    if row['面积'] >60 and row['面积'] <= 90:
        return '[60,90]'
    if row['面积'] >90 and row['面积'] <= 120:
        return '[90,120]'
    if row['面积'] >120 and row['面积'] <= 150:
        return '[120,150]'
    if row['面积'] >150 :
        return '[150,-]'
    return '[未知]'    

def total_price_analysis_by_square(df):
    #增加一列[面积区间]
    df['面积区间'] = df.apply(cal_square_district,args=(),axis=1)
    #获取要分析的数据行和列
    analysis_df = df.loc[:,['面积区间','总价']]
    analysis_df.loc[:,'面积区间'] = analysis_df.loc[:,'面积区间'].astype('str')
    #对面积区间列group by，然后按分组计算总价和均价的平均值
    group = analysis_df.groupby('面积区间')
    group_df = group.mean()
    group_df.loc[:,'总价'] = group_df.loc[:,'总价'].astype('int')
    print(group_df)
    
    bar = (
        Bar()
        .add_xaxis(group_df.index.tolist())
        .add_yaxis("总价均价",group_df["总价"].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="按面积区间的房屋总价分析"))
    )
    
    return bar.render_embed()

def unit_price_analysis_by_square(df):
    #增加一列[面积区间]
    df['面积区间'] = df.apply(cal_square_district,args=(),axis=1)
    #获取要分析的数据行和列
    analysis_df = df.loc[:,['面积区间','均价']]
    analysis_df.loc[:,'面积区间'] = analysis_df.loc[:,'面积区间'].astype('str')
    #对面积区间列group by，然后按分组计算总价和均价的平均值
    group = analysis_df.groupby('面积区间')
    group_df = group.mean()
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    print(group_df)
    
    bar = (
        Bar()
        .add_xaxis(group_df.index.tolist())
        .add_yaxis("单价均价",group_df["均价"].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="按面积区间的房屋单价分析"))
    )
    
    return bar.render_embed()
    
if __name__ == '__main__':
    total_price_analysis_by_square()