"""
@author kingfish
import在导入文件的时候，会自动把所有暴露在外面的代码全都执行一遍。
因此，如果你要把一个东西封装成模块，又想让它可以执行的话，你必须将要执行的代码放在 if __name__ == '__main__'下面

这里放在if __name__ == '__main__'下面的代码，在本模块被其他模块import的时候，不会执行
但模块自身执行的时候，会执行这部分代码
"""

# utils_with_main.py

def get_sum(a, b):
    return a + b

if __name__ == '__main__':
    print('testing')
    print('{} + {} = {}'.format(1, 2, get_sum(1, 2)))