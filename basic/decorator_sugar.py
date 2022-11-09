"""
@author kingfish
这里的@，我们称之为语法糖，@my_decorator就相当于前面的greet=my_decorator(greet)语句，只不过更加简洁。
因此，如果你的程序中有其它函数需要做类似的装饰，你只需在它们的上方加上@decorator就可以了，这样就大大提高了函数的重复利用和程序的可读性
"""

def my_decorator(func):
    def wrapper():
        print('wrapper of decorator before')
        func()
        print("wrapper of decorator after")
    return wrapper

@my_decorator
def greet():
    print('hello world')

greet()