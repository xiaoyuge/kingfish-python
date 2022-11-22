"""
读取excel数据，分析数据并生成图表
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
from pyecharts.commons.utils import JsCode
    
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

def unit_price_analysis_by_estate(df):
    #获取要分析的数据列
    analysis_df = df.loc[:,['小区名称','均价']]
    analysis_df.loc[:,'小区名称'] = analysis_df.loc[:,'小区名称'].astype('str')
    #对小区名称分组，然后按照分组计算单价均价
    group = analysis_df.groupby('小区名称',as_index=False)
    group_df = group.mean()
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    #按照均价列降序排序
    group_df.sort_values('均价',ascending=False, inplace=True)
    #取Top10
    top10_df = group_df.head(10)
    #为了横向柱状图展示，再从低到高排序一下
    top10_df.sort_values('均价',ascending=True,inplace=True)
    print(top10_df)  

    bar = (
        Bar(init_opts=opts.InitOpts(width="1500px"))
        .add_xaxis(top10_df['小区名称'].tolist())
        .add_yaxis("房价单价",top10_df['均价'].tolist())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="苏州小区房价TOP10"),xaxis_opts=opts.AxisOpts(axislabel_opts={'interval':'0'}))
    )
    
    return bar.render_embed()

def unit_price_analysis_by_district(df):
    #获取要分析的数据列
    analysis_df = df.loc[:,['区','均价']]
    analysis_df.loc[:,'区'] = analysis_df.loc[:,'区'].astype('str')
    #对小区名称分组，然后按照分组计算单价均价
    group = analysis_df.groupby('区',as_index=False)
    group_df = group.mean()
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    #按照均价列降序排序
    group_df.sort_values('均价',ascending=True, inplace=True)
    print(group_df)  

    bar = (
        Bar(init_opts=opts.InitOpts(width="1500px"))
        .add_xaxis(group_df['区'].tolist())
        .add_yaxis("房价单价",group_df['均价'].tolist())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="苏州各区房价排行榜"),xaxis_opts=opts.AxisOpts(axislabel_opts={'interval':'0'}))
    )
    
    return bar.render_embed()

def add_sale_estate_col(row):
    return 0

def sale_estate_analysis_by_year(df):
    df.loc[:,'待售房屋数'] = df.apply(add_sale_estate_col,axis=1)
    analysis_df = df.loc[:,['建筑年份','待售房屋数']]
    analysis_df.dropna(inplace=True)
    
    group = analysis_df.groupby('建筑年份',as_index=False)
    group_df = group.count()
    group_df.loc[:,'待售房屋数'] = group_df.loc[:,'待售房屋数'].astype('int')
    print(group_df)
    
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px', bg_color='white'))
    pie.add("pie",[list(z) for z in zip(group_df['建筑年份'].tolist(),group_df['待售房屋数'].tolist())]
        ,radius=['40%', '60%']
        ,center=['50%', '50%']
        ,label_opts=opts.LabelOpts(
            position="outside",
            formatter="{d}%",)
        ).set_global_opts(
            title_opts=opts.TitleOpts(title='不同建筑年份的待售二手房数', pos_left='300', pos_top='20',
            title_textstyle_opts=opts.TextStyleOpts(color='black', font_size=16)),
            legend_opts=opts.LegendOpts(is_show=False))

    return pie.render_embed()