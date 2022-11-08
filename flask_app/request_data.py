"""
@author kingfish
用falsk开发的web应用
各种处理请求数据，包括
1.路径带参数
2.request获取路径参数
3.request获取post数据
4.request获取form数据
"""

from flask import Flask,render_template,request
import json

app = Flask(__name__)

#路径带参数
@app.route('/user/<username>')
def get_user_by_path(username):
    return "hello %s" %username

#同样路径，用post访问
@app.route('/user/<username>',methods=["POST"])
def get_user_by_path_post(username):
    return "hello %s by post" %username

#探索一下request获取路径参数
@app.route('/url_data')
def get_url_data():
    print('-----------------------获取args---------------------')
    arga = request.args.get('a')
    argb = request.args.get('b')
    print("参数a是 %s" %arga + " 参数b是 %s" %argb)
    return "Request Successful"

#探索一下request获取post参数
@app.route('/json_data',methods=["POST","GET"])
def get_post_data():
    print('-----------------------获取data---------------------')
    jsonData = request.data
    jsonData = json.loads(jsonData)
    print(jsonData)
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

#探索一下request获取请求头数据
@app.route('/header_data')
def get_header_data():
    print('-----------------------获取User-Agent---------------------')
    print(request.headers.get('User-Agent'))
    print('-----------------------获取cookies---------------------')
    print(request.cookies)
    print(request.cookies.get("token")) 
    return "Request Successful"

if __name__ == '__main__':
    app.run()