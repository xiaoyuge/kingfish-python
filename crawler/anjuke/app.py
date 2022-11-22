"""
启动一个web网站，展示不同的分析数据图表
"""
from flask import Flask
import drawChart as dbc
import pandas as pd

app = Flask(__name__)
#读取要分析的数据
fpath = 'crawler/anjuke/suzhouSecondHouse-2022-11-22-200页.xlsx'
df = pd.read_excel(fpath,sheet_name="Sheet1",header=[0],engine='openpyxl')

@app.route("/barchart")
def bar_chart():    
    str = dbc.draw_bar_chart()
    print(str)
    return str   

@app.route("/total_price_analysis_by_suqare")
def bar_total_price_analysis_by_square():
    str = dbc.total_price_analysis_by_square(df)
    return str

@app.route("/unit_price_analysis_by_suqare")
def bar_unit_price_analysis_by_square():
    str = dbc.unit_price_analysis_by_square(df)
    return str

if __name__ == "__main__":
    app.run()