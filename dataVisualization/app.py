"""
@author kingfish
读取excel数据，画柱状图
"""
from flask import Flask,render_template
import drawBarChart.draw_bar_chart as dbc

app = Flask(__name__)

@app.route("/barchart")
def bar_chart():
    str = dbc.draw_bar_chart()
    return str   

if __name__ == "__main__":
    app.run()