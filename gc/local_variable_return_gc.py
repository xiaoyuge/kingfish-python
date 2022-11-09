"""
@author kingfish
创建一个较大的列表，，赋值给一个函数局部变量，在函数执行完后return变量，分别查看内存使用情况

可以看到，如果我们把生成的列表返回，然后在主程序中接收，那么引用依然存在，垃圾回收就不会被触发，大量内存仍然被占用着
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
    return a
    
if __name__ == "__main__":
    a = func()
    show_memory_info('finished')