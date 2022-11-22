"""
启动一个web网站，展示不同的分析数据图表
"""
from flask import Flask
import drawChart as dbc

app = Flask(__name__)

@app.route("/barchart")
def bar_chart():    
    str = dbc.draw_bar_chart()
    print(str)
    return str   

if __name__ == "__main__":
    app.run()