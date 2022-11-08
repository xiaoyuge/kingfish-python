"""
@author kingfish
用falsk开发的web应用
1.读取本地文件数据
2.将数据转换为json数据返回
"""

from flask import Flask,render_template
import json

app = Flask(__name__)

#读取文件，返回数据
def read_data():
    #读取文件
    datas = []
    with open("datas/beijing_tianqi/beijing_tianqi_2018.csv") as fin:
        for line in fin:
            if line.startswith("ymd"):
                continue
            line = line[:-1]
            ymd,bWendu,yWendu,tianqi,fengxiang,fengli,aqi,aqiInfo,aqiLevel = line.split(",")
            datas.append((ymd,bWendu,yWendu,tianqi,fengxiang,fengli,aqi,aqiInfo,aqiLevel))
    return datas
    
@app.route('/returnJson')
def return_json():
    datas = read_data()
    return json.dumps(datas)

if __name__ == "__main__":
    app.run()

