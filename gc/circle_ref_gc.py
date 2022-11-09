"""
@author kingfish
循环引用：
a 和 b 互相引用，并且，作为局部变量，在函数 func 调用结束后，a 和 b 这两个指针从程序意义上已经不存在了。
但是很明显，依然有内存占用，因为互相引用，导致它们的引用数都不为 0
"""

from local_variable_gc import show_memory_info

def func():
    show_memory_info('initial')
    a = [i for i in range(10000000)]
    b = [i for i in range(10000000)]
    show_memory_info('after a, b created')
    a.append(b)
    b.append(a)

func()
show_memory_info('finished')
