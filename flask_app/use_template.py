"""
@author kingfish
用falsk开发的web应用
各种返回数据，包括使用模版
"""

from flask import Flask,render_template,request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

#增加一个新的路由路径
@app.route('/hello')
def hello_world2():
    return 'Hello World 2!'

#除了返回普通文本，还可以返回html片段
@app.route('/hi')
def hi_world():
    return """
        <html>
            <body>
                <h1 style="color:#e00;">Hi World !</h1>
            </body>
        </html>
    """

#将html片段分离为一个单独的模板文件
@app.route('/hitpl')
def hi_tpl():
    return render_template("hello_world.html")

#传递数据给模板文件
@app.route('/hitpldt')
def hi_tpl_dt():
    data = "hi world from data!"
    return render_template("hello_world_from_data.html",data=data)

#传递列表数据给模板文件，使用for和if处理数据
@app.route('/use_template')
def use_template():
    datas = [(1,"name1"),(2,"name2"),(3,"name3")]
    title = "学生信息"
    return render_template("use_template.html",datas = datas,title = title)

if __name__ == '__main__':
    app.run()