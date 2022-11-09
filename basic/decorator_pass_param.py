"""
@author kingfish
可以在对应的装饰器函数 wrapper() 上，加上相应的参数，来实现原函数 greet() 的参数需传递给装饰器
如果有多个参数需要传递，则可使用*args和**kwargs
args 是 arguments 的缩写，表示位置参数；kwargs 是 keyword arguments 的缩写，表示关键字参数
"""

def my_decorator(func):
    def wrapper(message):
        print('wrapper of decorator')
        func(message)
    return wrapper

@my_decorator
def greet(message):
    print(message)

greet('hello world')

def my_decorator2(func):
    def wrapper(*args, **kwargs):
        print('wrapper of decorator')
        func(*args, **kwargs)
    return wrapper

@my_decorator2
def greet2(*args):
    for arg in args:
        print(arg)
        
greet2(123,"ahah",[1,2,3])
