"""
@author kingfish
创建一个较大的列表，赋值给一个全局变量，在创建前后分别查看内存使用情况

可以看到，调用函数 func()，在列表 a 被创建之后，内存占用迅速增加。而在函数调用结束后，内存没有很大变化
因为，global a 表示将 a 声明为全局变量。那么，即使函数返回后，列表的引用依然存在，于是对象就不会被垃圾回收掉，依然占用大量内存
"""

import os
import psutil

# 显示当前 python 程序占用的内存大小
def show_memory_info(hint):
    pid = os.getpid()
    print("current python process id: %d"%pid)
    p = psutil.Process(pid)
    
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print('{} memory used: {} MB'.format(hint, memory))
    

def func():
    show_memory_info('initial')
    global a 
    a = [i for i in range(10000000)]
    show_memory_info('after a created')
    
if __name__ == "__main__":
    func()
    show_memory_info('finished')