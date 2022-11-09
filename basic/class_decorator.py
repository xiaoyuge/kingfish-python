"""
@author kingfish
类也可以作为装饰器。类装饰器主要依赖于函数__call__()，每当你调用一个类的示例时，函数__call__()就会被执行一次

这里，我们定义了类 Count，初始化时传入原函数 func()，而__call__()函数表示让变量 num_calls 自增 1，然后打印，并且调用原函数。
因此，在我们第一次调用函数 example() 时，num_calls 的值是 1，而在第二次调用时，它的值变成了 2
"""

class Count:
    def __init__(self, func):
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))
        return self.func(*args, **kwargs)

@Count
def example():
    print("hello world")

example()

example()

