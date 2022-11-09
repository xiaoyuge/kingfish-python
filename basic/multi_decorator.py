"""
@author kingfish
Python 也支持多个装饰器，比如写成下面这样的形式：

@decorator1
@decorator2
@decorator3
def func():
    ...
    
它的执行顺序从里到外，所以上面的语句也等效于下面这行代码

decorator1(decorator2(decorator3(func)))
"""
import functools

def my_decorator1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('execute decorator1')
        func(*args, **kwargs)
    return wrapper


def my_decorator2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('execute decorator2')
        func(*args, **kwargs)
    return wrapper


@my_decorator1
@my_decorator2
def greet(message):
    print(message)


greet('hello world')