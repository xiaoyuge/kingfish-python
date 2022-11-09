"""
@author kingfish
Python的引用计数机制
注意：
a、b、c、d、e、f、g 这些变量全部指代的是同一个对象，而 sys.getrefcount() 函数并不是统计一个指针，而是要统计一个对象被引用的次数，
所以最后一共会有八次引用。
"""

import sys

a = []

print(sys.getrefcount(a)) # 两次

b = a

print(sys.getrefcount(a)) # 三次

c = b
d = b
e = c
f = e
g = d

print(sys.getrefcount(a)) # 八次