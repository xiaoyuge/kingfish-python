"""
@author kingfish
objgraph是一个非常好用的可视化引用关系的包，推荐两个函数
1. show_refs()
2.  show_backrefs()
objgraph不是标准库，需要手动安装：pip install objgraph
图片渲染和查看需要安装：pip install graphviz xdot
"""

import objgraph

a = [1, 2, 3]
b = [4, 5, 6]

a.append(b)
b.append(a)

objgraph.show_refs([a],filename="refs-graph.png")

objgraph.show_backrefs([a],filename="backrefs-graph.png")