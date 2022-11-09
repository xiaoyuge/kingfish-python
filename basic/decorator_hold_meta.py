"""
@author kingfish
函数被装饰以后，它的元信息变了。元信息告诉我们“它不再是以前的那个函数，而是被 wrapper() 函数取代了”

为了解决这个问题，我们通常使用内置的装饰器@functools.wrap，它会帮助保留原函数的元信息（也就是将原函数的元信息，拷贝到对应的装饰器函数里）
"""

import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('wrapper of decorator')
        func(*args, **kwargs)
    return wrapper
    
@my_decorator
def greet(message):
    print(message)

print(greet.__name__)
