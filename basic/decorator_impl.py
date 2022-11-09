"""
@author kingfish
这段代码演示了装饰器的原理
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
