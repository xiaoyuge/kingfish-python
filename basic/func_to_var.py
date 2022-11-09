"""
@author kingfish
函数赋予变量
"""

def func(message):
    print('Got a message: {}'.format(message))

#函数 func 赋予了变量 send_message
send_message = func
#调用 send_message，就相当于是调用函数 func()
send_message('hello world')
