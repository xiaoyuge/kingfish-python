"""
@author kingfish
这段代码演示了装饰器的原理
这里的函数 my_decorator() 就是一个装饰器，它把真正需要执行的函数 greet() 包裹在其中，并且改变了它的行为，但是原函数 greet() 不变
"""

def greet_decorator(func):
    def wrapper():
        print('wrapper of decorator before')
        func()
        print("wrapper of decorator after")
    return wrapper

def greet():
    print('hello world')

greet_wrapper = greet_decorator(greet)
greet_wrapper()
