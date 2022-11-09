"""
@author kingfish
这里对比一下用numpy进行数组计算和直接使用Python，一个是简洁性，一个是性能
当n=1000*10000的时候，我的机器的结果是：
python_sum time is  10.844529867172241
numpy_sum time is  0.4988579750061035
"""
import numpy as np
import time

#用native的方式实现两个数组相加
def python_sum(n):
    a = [i**2 for i in range(n)]
    b = [i**3 for i in range(n)]
    
    c = []
    
    for i in range(n):      
        c.append(a[i]+b[i])
        
    return c

#用Numpy的方式实现两个数组相加
def numpy_sum(n):
    a = np.arange(n)**2
    b = np.arange(n)**3
    return a+b

if __name__ == "__main__":
    start = time.time()
    c = python_sum(1000*10000)
    end = time.time()
    #print(c)
    print("python_sum time is ",end-start)
    
    start = time.time()
    c = numpy_sum(1000*10000)
    end = time.time()
    #print(c)
    print("numpy_sum time is ",end-start)