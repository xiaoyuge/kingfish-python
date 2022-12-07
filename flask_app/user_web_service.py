"""
@author kingfish
用户管理web服务接口：http+json
"""

from flask import Flask,render_template,request
import db
import json

app = Flask(__name__)

#新增用户接口
@app.route('/add_user',methods=["POST"])
def do_add_user():
    #获取json数据
    jsonData = request.data
    jsonData = json.loads(jsonData)
    #解析json拿到用户数据
    username = jsonData['username']
    age = jsonData['age']
    sex = jsonData['sex']
    email = jsonData['email']
    #拼接sql
    sql = f"""
    INSERT INTO user (name,age,sex,email)
    values ('{username}',{age},'{sex}','{email}')"""
    print(sql)
    #执行sql插入数据库
    db.insert_or_update(sql)
    #从数据库查询数据
    sql = 'select id,name,sex,age,email from user'
    datas = db.query_data(sql)
    return 'Success'

#查询用户接口
@app.route('/query_user/<user_id>')
def show_user_detail(user_id):
    sql = f'select id,name,sex,age,email from user where id = {user_id}'
    datas = db.query_data(sql)
    print(datas)
    return json.dumps(datas)


if __name__ == '__main__':
    app.run()