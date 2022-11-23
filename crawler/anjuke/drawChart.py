"""
读取excel数据，分析数据并生成图表
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie,Scatter,WordCloud,Map
import numpy as np
import jieba
import jieba.analyse
    
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

def order_layout_ascending(row):
    if row['室'] == '1室':
        return 0
    if row['室'] == '2室':
        return 1
    if row['室'] == '3室':
        return 2
    if row['室'] == '4室':
        return 3
    if row['室'] == '5室':
        return 4
    if row['室'] == '6室':
        return 5

def unit_price_analysis_by_layout(df,isembed):
    #增加一列[面积区间]
    df['面积区间'] = df.apply(cal_square_district,args=(),axis=1)
    #获取要分析的数据行和列
    analysis_df = df.loc[:,['室','均价']]
    analysis_df.loc[:,'室'] = analysis_df.loc[:,'室'].astype('str')
    #对面积区间列group by，然后按分组计算总价和均价的平均值
    group = analysis_df.groupby('室',as_index=False)
    group_df = group.mean()
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    #给室这个字段排个序
    group_df['order'] = group_df.apply(order_layout_ascending,axis=1)
    group_df.sort_values('order',ascending=True, inplace=True)
    
    bar = (
        Bar()
        .add_xaxis(group_df['室'].tolist())
        .add_yaxis("单价均价",group_df["均价"].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="苏州二手房按户型的房屋单价"),
                         legend_opts=opts.LegendOpts(is_show=False))
    )
    
    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return bar.render_embed()
    else:
        return bar


def order_square_ascending(row):
    if row['面积区间'] == '[0,60]':
        return 0
    if row['面积区间'] == '[60,90]':
        return 1
    if row['面积区间'] == '[90,120]':
        return 2
    if row['面积区间'] == '[120,150]':
        return 3
    if row['面积区间'] == '[150,-]':
        return 4

def unit_price_analysis_by_square(df,isembed):
    #增加一列[面积区间]
    df['面积区间'] = df.apply(cal_square_district,args=(),axis=1)
    #获取要分析的数据行和列
    analysis_df = df.loc[:,['面积区间','均价']]
    analysis_df.loc[:,'面积区间'] = analysis_df.loc[:,'面积区间'].astype('str')
    #对面积区间列group by，然后按分组计算总价和均价的平均值
    group = analysis_df.groupby('面积区间',as_index=False)
    group_df = group.mean()
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    #把面积区间按从小到大排个序
    group_df['order'] = group_df.apply(order_square_ascending,axis=1)
    group_df.sort_values('order',ascending=True, inplace=True)
    
    bar = (
        Bar()
        .add_xaxis(group_df['面积区间'].tolist())
        .add_yaxis("单价均价",group_df["均价"].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="苏州二手房按面积区间的房屋单价"),
            legend_opts=opts.LegendOpts(is_show=False))
    )
    
    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return bar.render_embed()
    else:
        return bar

def unit_price_analysis_by_estate(df,isembed):
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

    bar = (
        Bar(init_opts=opts.InitOpts(width="1500px"))
        .add_xaxis(top10_df['小区名称'].tolist())
        .add_yaxis("房价单价",top10_df['均价'].tolist())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="苏州各小区二手房房价TOP10"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts={'interval':'0'}),
                         legend_opts=opts.LegendOpts(is_show=False))
    )
    
     #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return bar.render_embed()
    else:
        return bar

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

    bar = (
        Bar(init_opts=opts.InitOpts(width="1500px"))
        .add_xaxis(group_df['区'].tolist())
        .add_yaxis("房价单价",group_df['均价'].tolist())
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="苏州各区域二手房房价排行榜"),xaxis_opts=opts.AxisOpts(axislabel_opts={'interval':'0'}))
    )
    
    return bar.render_embed()

def add_sale_estate_col(row):
    return 0

def sale_estate_analysis_by_year(df,isembed):
    df.loc[:,'待售房屋数'] = df.apply(add_sale_estate_col,axis=1)
    analysis_df = df.loc[:,['建筑年份','待售房屋数']]
    analysis_df.dropna(inplace=True)
    
    group = analysis_df.groupby('建筑年份',as_index=False)
    group_df = group.count()
    group_df.loc[:,'待售房屋数'] = group_df.loc[:,'待售房屋数'].astype('int')
    
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='600px', bg_color='white'))
    pie.add("pie",[list(z) for z in zip(group_df['建筑年份'].tolist(),group_df['待售房屋数'].tolist())]
        ,radius=['40%', '60%']
        ,center=['50%', '50%']
        ,label_opts=opts.LabelOpts(
            position="outside",
            formatter="{b}:{c}:{d}%",)
        ).set_global_opts(
            title_opts=opts.TitleOpts(title='苏州二手房不同建筑年份的待售数量', pos_left='300', pos_top='20',
            title_textstyle_opts=opts.TextStyleOpts(color='black', font_size=16)),
            legend_opts=opts.LegendOpts(is_show=False))

    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return pie.render_embed()
    else:
        return pie

def unit_price_analysis_by_histogram(df,isembed):
    hist,bin_edges = np.histogram(df['均价'],bins=100)
    
    bar = (
        Bar()
        .add_xaxis([str(x) for x in bin_edges[:-1]])
        .add_yaxis('价格分布',[float(x) for x in hist],category_gap=0)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='苏州二手房房价-单价分布-直方图',pos_left='center'),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    
     #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return bar.render_embed()
    else:
        return bar


def total_price_analysis_by_histogram(df,isembed):
    hist,bin_edges = np.histogram(df['总价'],bins=100)
    
    bar = (
        Bar()
        .add_xaxis([str(x) for x in bin_edges[:-1]])
        .add_yaxis('价格分布',[float(x) for x in hist],category_gap=0)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='苏州二手房房价-总价分布-直方图',pos_left='center'),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    
    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return bar.render_embed()
    else:
        return bar

def unit_price_analysis_by_scatter(df,isembed):
    
    df.sort_values('面积',ascending=True, inplace=True)
     
    square = df['面积'].to_list()
    unit_price = df['均价'].to_list()
     
    scatter = (
         Scatter()
         .add_xaxis(xaxis_data=square)
         .add_yaxis(
             series_name='',
             y_axis=unit_price,
             symbol_size=4,
             label_opts=opts.LabelOpts(is_show=False)
         )
         .set_global_opts(
             xaxis_opts=opts.AxisOpts(type_='value'),
             yaxis_opts=opts.AxisOpts(type_='value'),
             title_opts=opts.TitleOpts(title='苏州二手房面积-单价关系图',pos_left='center')
         )
     )
     
    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return scatter.render_embed()
    else:
        return scatter
 
 
def hot_word_analysis_by_wordcloud(df,isembed):
    txt = ''
    for index,row in df.iterrows():
        txt = txt+ str(row['待售房屋']) + ';'+ str(row['标签']) + '\n'
     
    word_weights = jieba.analyse.extract_tags(txt,topK=100,withWeight=True)
     
    word_cloud=(
        WordCloud()
        .add(series_name='高频词语',data_pair=word_weights,word_size_range=[10,100])
        .set_global_opts(
            title_opts=opts.TitleOpts(
            title='苏州二手房销售热度词',
            title_textstyle_opts=opts.TextStyleOpts(font_size=23),
            pos_left='center'
            )
        )
    )
    
    #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return word_cloud.render_embed()
    else:
        #png_name = 'hot_word_analysis_by_wordcloud.png'
        #make_snapshot(snapshot, word_cloud.render(), f"crawler/anjuke/static/{png_name}")
        #return png_name
        return word_cloud
    
    
def transform_name(row):
    district_name = row['区'].strip()
    if district_name == '吴中' or district_name == '相城' or district_name == '吴江' or district_name == '虎丘' or district_name == '姑苏':
        district_name = district_name + '区'
    if district_name == '常熟' or district_name == '张家港' or district_name == '太仓':
        district_name = district_name + '市'
    return district_name
    
def unit_price_analysis_by_map(df,isembed):
    data = []
    #获取要分析的数据列
    analysis_df = df.loc[:,['区','均价']]
    #按区列分组
    group_df = analysis_df.groupby('区',as_index=False)
    #根据分组对均价列求平均值
    group_df = group_df.mean('均价')
    #print(group_df)
    #将区的名字做一下转换，为下面的地图匹配做准备
    group_df['区'] = group_df.apply(transform_name,axis=1)
    group_df.loc[:,'均价'] = group_df.loc[:,'均价'].astype('int')
    #将数据转换成map需要的数据格式
    for index,row in group_df.iterrows():
        district_array = [row['区'],row['均价']]
        data.append(district_array)
    
    map = (
        Map()
        .add('苏州各区域二手房房价',data,'苏州')
        .set_global_opts(
            title_opts=opts.TitleOpts(title='苏州各区域二手房房价地图',pos_left='center'),
            visualmap_opts=opts.VisualMapOpts(max_=26000),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
     #判断是否单独显示，还是和其他图表一起显示
    if isembed:
        return map.render_embed()
    else:
        #png_name = 'unit_price_analysis_by_map.png'
        #make_snapshot(snapshot, map.render(), f"crawler/anjuke/static/{png_name}")
        #return png_name
        return map