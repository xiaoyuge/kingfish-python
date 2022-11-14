"""
@author kingfish
两个结构相同的excel文件，拼接到一起，输出到一个文件
"""

import pandas as pd
import os

#用来存放读取的多个文件的内容
dfs = []

#文件的读取目录路径
fpath = "datas/merge_excel_multi_sheets/"

# read all excel 's sheet append to dfs

for fname in os.listdir(fpath):
    if fname.endswith(".xls") and fname != "final.xls":
        #拼接一下完整的文件路径
        fname = fpath + fname
        
        df = pd.read_excel(
            fname,
            header=None,
            sheet_name=None
        )
        #将读取的文件内容加入列表
        dfs.extend(df.values())

# 将多个文件的内容拼接在一起
result = pd.concat(dfs)

# output excel
result.to_excel("%sfinal.xls"%fpath, index=False)