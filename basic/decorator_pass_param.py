"""
@author kingfish
可以在对应的装饰器函数 wrapper() 上，加上相应的参数，来实现原函数 greet() 的参数需传递给装饰器
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