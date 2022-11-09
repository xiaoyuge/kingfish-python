"""
@author kingfish
如果我想要定义一个参数，来表示装饰器内部函数被执行的次数，那么就可以写成下面这种形式
"""

def repeat(num):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(num):
                print('wrapper of decorator')
                func(*args, **kwargs)
        return wrapper
    return my_decorator


@repeat(4)
def greet(message):
    print(message)

greet('hello world')