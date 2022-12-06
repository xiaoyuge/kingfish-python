"""
@author kingfish
用户管理web应用
"""

from flask import Flask,render_template,request
import db

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/show_add_user')
def add_user():
    return render_template('show_add_user.html')

@app.route('/do_add_user',methods=["POST"])
def do_add_user():
    #从form拿数据
    print(request.form)
    form_data = request.form
    username = form_data.get('username')
    age = form_data.get('age')
    sex = form_data.get('sex')
    email = form_data.get('email')
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
    return render_template('show_user_list.html',datas=datas)

@app.route('/show_user_detail/<id>')
def show_user_detail(id):
    sql = f'select id,name,sex,age,email from user where id = {id}'
    datas = db.query_data(sql)
    print(datas)
    return render_template('show_user_detail.html',datas=datas)

if __name__ == '__main__':
    app.run()