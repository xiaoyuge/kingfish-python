"""
@author kingfish
用falsk开发的web应用
"""

from flask import Flask,render_template

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
    return render_template("helloworld.html")

#传递数据给模板文件
@app.route('/hitpldt')
def hi_tpl_dt():
    data = "hi world from data!"
    return render_template("helloworldfromdata.html",data=data)

#路径带参数
@app.route('/user/<username>')
def get_user(username):
    return "hello %s" %username

#同样路径，用post访问
@app.route('/user/<username>',methods=["POST"])
def get_user_by_post(username):
    return "hello %s by post" %username

if __name__ == '__main__':
    app.run()