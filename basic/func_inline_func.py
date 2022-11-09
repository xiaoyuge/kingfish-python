"""
@author kingfish
在函数里定义函数，也即数的嵌套
"""

#在函数 func() 里又定义了新的函数 get_message()，调用后作为 func() 的返回值返回
def func(message):
    def get_message(message):
        print('Got a message: {}'.format(message))
    return get_message(message)

func('hello world')