"""
@author kingfish
用falsk开发的web应用
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

#路径带参数
@app.route('/user/<username>')
def get_user(username):
    return "hello %s" %username

#同样路径，用post访问
@app.route('/user/<username>',methods=["POST"])
def get_user_by_post(username):
    return "hello %s by post" %username

#探索一下request获取数据
@app.route('/data',methods=["POST","GET"])
def get_request_data():
    print('-----------------------获取args---------------------')
    arga = request.args.get('a')
    argb = request.args.get('b')
    print("参数a是 %s" %arga + " 参数b是 %s" %argb)
    print(request.headers.get('User-Agent'))
    print('-----------------------获取data---------------------')
    jsonData = request.data
    jsonData = json.loads(jsonData)
    print(jsonData)
    print('-----------------------获取cookies---------------------')
    print(request.cookies)
    print(request.cookies.get("token")) 
    return "Request Successful"

#从表单获取数据
@app.route('/formData',methods=["POST","GET"])
def get_form_data():
    form = request.form
    print(form)
    username = form.get("username")
    print(username)
    password = form.get("password")
    print(password)
    return "Post form Successful"

#使用模版
@app.route('/user_template')
def use_template():
    datas = [(1,"name1"),(2,"name2"),(3,"name3")]
    title = "学生信息"
    return render_template("use_template.html",datas = datas,title = title)

if __name__ == '__main__':
    app.run()