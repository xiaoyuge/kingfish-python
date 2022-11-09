"""
@author kingfish
创建一个较大的列表，在创建前后分别查看内存使用情况
查看当前Python进程的内存使用情况

可以看到，调用函数 func()，在列表 a 被创建之后，内存占用迅速增加。而在函数调用结束后，内存则返回正常
因为，函数内部声明的列表 a 是局部变量，在函数返回后，局部变量的引用会注销掉
此时，列表 a 所指代对象的引用数为 0，Python 便会执行垃圾回收，因此之前占用的大量内存就又回来了
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
    a = [i for i in range(10000000)]
    show_memory_info('after a created')
    
if __name__ == "__main__":
    func()
    show_memory_info('finished')