"""
@author kingfish
把函数当作参数，传入另一个函数中
"""

def get_message(message):
    return 'Got a message: ' + message

def root_call(func, message):
    print(func(message))
    
#函数 get_message 以参数的形式，传入了函数 root_call() 中然后调用它
root_call(get_message, 'hello world')
