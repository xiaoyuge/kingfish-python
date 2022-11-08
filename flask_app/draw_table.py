"""
@author kingfish
用falsk开发的web应用
1.读取文件
2.画网页表格
"""

from flask import Flask,render_template

app = Flask(__name__)

#读取文件，画表格
@app.route("/draw_table")
def draw_table():
    #读取文件
    datas = []
    with open("datas/beijing_tianqi/beijing_tianqi_2018.csv") as fin:
        for line in fin:
            if line.startswith("ymd"):
                continue
            line = line[:-1]
            ymd,bWendu,yWendu,tianqi,fengxiang,fengli,aqi,aqiInfo,aqiLevel = line.split(",")
            datas.append((ymd,bWendu,yWendu,tianqi,fengxiang,fengli,aqi,aqiInfo,aqiLevel))
    
    #返回表格数据给模版
    return render_template("draw_table.html",datas = datas)
    pass

if __name__ == "__main__":
    app.run()

