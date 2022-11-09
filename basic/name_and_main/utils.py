"""
@author kingfish
utils暴露在被调用函数外的代码，在被import的时候，会被自动执行
"""
# utils.py

def get_sum(a, b):
    return a + b

print('testing')
print('{} + {} = {}'.format(1, 2, get_sum(1, 2)))