"""
@author kingfish
函数的返回值也可以是函数对象（闭包）
"""

#函数 func_closure() 的返回值是函数对象 get_message 本身
def func_closure():
    def get_message(message):
        print('Got a message: {}'.format(message))
    return get_message

send_message = func_closure()
send_message('hello world')