"""
启动一个web网站，展示不同的分析数据图表
"""
from flask import Flask,render_template
import drawChart as dbc
import pandas as pd

app = Flask(__name__)

#读取要分析的数据
fpath = 'crawler/anjuke/data/suzhouSecondHouse-2022-11-22-200页.xlsx'
df = pd.read_excel(fpath,sheet_name="Sheet1",header=[0],engine='openpyxl')
df.drop_duplicates(keep='first',inplace=True) 

@app.route("/unit_price_analysis_by_layout")
def bar_unit_price_analysis_by_layout():
    result = dbc.unit_price_analysis_by_layout(df,True)
    return  result

@app.route("/unit_price_analysis_by_suqare")
def bar_unit_price_analysis_by_square():
    result = dbc.unit_price_analysis_by_square(df,True)
    return result

@app.route("/unit_price_analysis_by_estate")
def bar_unit_price_analysis_by_estate():
    str = dbc.unit_price_analysis_by_estate(df,True)
    return str

@app.route("/unit_price_analysis_by_district")
def bar_unit_price_analysis_by_district():
    str = dbc.unit_price_analysis_by_district(df)
    return str

@app.route("/pie_sale_estate_analysis_by_year")
def pie_sale_estate_analysis_by_year():
    str = dbc.sale_estate_analysis_by_year(df,True)
    return str

@app.route("/histogram_unit_price_analysis")
def histogram_unit_price_analysis():
    str = dbc.unit_price_analysis_by_histogram(df,True)
    return str

@app.route("/histogram_total_price_analysis")
def histogram_total_price_analysis():
    str = dbc.total_price_analysis_by_histogram(df,True)
    return str

@app.route("/scatter_unit_price_analysis")
def scatter_unit_price_analysis():
    str = dbc.unit_price_analysis_by_scatter(df,True)
    return str

@app.route("/word_cloud_hot_word_analysis")
def word_cloud_hot_word_analysis():
    str = dbc.hot_word_analysis_by_wordcloud(df,True)
    return str

@app.route("/map_unit_price_analysis")
def map_unit_price_analysis():
    str = dbc.unit_price_analysis_by_map(df,True)
    return str

@app.route("/show_all_analysis_chart")
def show_all_analysis_chart():
    
    #获取按面积区间的单价分析数据
    unit_price_analysis_by_square = dbc.unit_price_analysis_by_square(df,False)
    #获取按室区分的单价分析数据
    unit_price_analysis_by_layout = dbc.unit_price_analysis_by_layout(df,False)
    #获取苏州各小区二手房房价TOP10
    unit_price_analysis_by_estate = dbc.unit_price_analysis_by_estate(df,False)
    #获取不同建筑年份的待售房屋数
    sale_estate_analysis_by_year = dbc.sale_estate_analysis_by_year(df,False)
    #苏州二手房房价-单价分布-直方图
    unit_price_analysis_by_histogram = dbc.unit_price_analysis_by_histogram(df,False)
    #苏州二手房房价-总价分布-直方图
    total_price_analysis_by_histogram = dbc.total_price_analysis_by_histogram(df,False)
    #苏州二手房面积-单价关系图
    unit_price_analysis_by_scatter = dbc.unit_price_analysis_by_scatter(df,False)
    #苏州二手房销售热度词
    #hot_word_analysis_by_wordcloud_png_name = dbc.hot_word_analysis_by_wordcloud(df,False)
    hot_word_analysis_by_wordcloud = dbc.hot_word_analysis_by_wordcloud(df,False)
    #苏州各区域二手房房价
    #unit_price_analysis_by_map_png_name = dbc.unit_price_analysis_by_map(df,False)
    unit_price_analysis_by_map = dbc.unit_price_analysis_by_map(df,False)
    
    
    return render_template("show_analysis_chart.html",
                            unit_price_analysis_by_square_option = unit_price_analysis_by_square.dump_options(),
                            unit_price_analysis_by_layout_option = unit_price_analysis_by_layout.dump_options(),
                            unit_price_analysis_by_estate_option = unit_price_analysis_by_estate.dump_options(),
                            sale_estate_analysis_by_year_option = sale_estate_analysis_by_year.dump_options(),
                            unit_price_analysis_by_histogram_option = unit_price_analysis_by_histogram.dump_options(),
                            total_price_analysis_by_histogram_option = total_price_analysis_by_histogram.dump_options(),
                            unit_price_analysis_by_scatter_option = unit_price_analysis_by_scatter.dump_options(),
                            hot_word_analysis_by_wordcloud_option = hot_word_analysis_by_wordcloud.dump_options(),
                            unit_price_analysis_by_map_option = unit_price_analysis_by_map.dump_options()
                           )

if __name__ == "__main__":
    app.run()