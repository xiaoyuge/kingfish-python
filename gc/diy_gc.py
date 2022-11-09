"""
@author kingfish
手动释放内存怎么做？
只需要先调用 del 来删除对象的引用；然后强制调用 gc.collect()，清除没有引用的对象，即可手动启动垃圾回收
"""

import gc
from local_variable_gc import show_memory_info

show_memory_info('initial')

a = [i for i in range(10000000)]

show_memory_info('after a created')

del a
gc.collect()

show_memory_info('finish')
print(a)
