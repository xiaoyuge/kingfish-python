"""
@author kingfish
Python的引用计数机制
注意：
1. sys.getrefcount() 这个函数，可以查看一个变量的引用次数，，getrefcount 本身也会引入一次计数；
2. 在函数调用发生的时候，会产生额外的两次引用，一次来自函数栈，另一个是函数参数；
"""

import sys

a = []

# 两次引用，一次来自 a，一次来自 getrefcount
print(sys.getrefcount(a))

def func(a):
    # 四次引用，a，python 的函数调用栈，函数参数，和 getrefcount
    print(sys.getrefcount(a))

func(a)

# 两次引用，一次来自 a，一次来自 getrefcount，函数 func 调用已经不存在
print(sys.getrefcount(a))
