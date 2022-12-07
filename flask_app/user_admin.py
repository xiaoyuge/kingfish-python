"""
@author kingfish
用户管理web应用
"""

import datetime
import os
from flask import Flask,render_template,request,send_from_directory
import db
import xlwt

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

def generate_excel_file(data_dir, file_name):
    fpath = os.path.join(data_dir,file_name)
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet("user")
    
    #先写表头
    for idx,name in enumerate(['id','name','sex','age','email']):
        worksheet.write(0,idx,name)
    
    #再写数据
    datas = db.query_data('select * from user')    
    for idx,data in enumerate(datas):
        worksheet.write(idx+1,0,data[0])
        worksheet.write(idx+1,1,data[1])
        worksheet.write(idx+1,2,data[2])
        worksheet.write(idx+1,3,data[3])
        worksheet.write(idx+1,4,data[4])
    
    workbook.save(fpath)

@app.route('/download_user_excel')
def download_user_excel():
    
    #要下载文件的目录和文件名
    data_dir = os.path.join(app.root_path,"downloads")
    now_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"user_{now_time}.xls"

    #生成excel文件
    generate_excel_file(data_dir, file_name)
    
    return send_from_directory(data_dir, file_name,as_attachment=True)

if __name__ == '__main__':
    app.run()