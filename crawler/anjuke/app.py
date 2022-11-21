"""
读取excel数据，画图
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