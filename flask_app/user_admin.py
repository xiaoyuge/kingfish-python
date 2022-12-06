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
    print(request.form)
    form_data = request.form
    username = form_data.get('username')
    age = form_data.get('age')
    sex = form_data.get('sex')
    email = form_data.get('email')
    sql = f"""
    INSERT INTO user (name,age,sex,email)
    values ('{username}',{age},'{sex}','{email}')"""
    print(sql)
    db.insert_or_update(sql)
    return 'Successful'

if __name__ == '__main__':
    app.run()