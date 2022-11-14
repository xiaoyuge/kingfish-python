"""
@author kingfish
两个结构相同的excel文件，拼接到一起，输出到一个文件
"""

import pandas as pd
import os

dfs = []

# read all excel 's sheet append to dfs
fpath = "datas/merge_excel_multi_sheets/"
for fname in os.listdir(fpath):
    if fname.endswith(".xls") and fname != "final.xls":
        fname = fpath + fname
        df = pd.read_excel(
            fname,
            header=None,
            sheet_name=None
        )
        dfs.extend(df.values())

# concat
result = pd.concat(dfs)

# output excel
result.to_excel("./final.xls", index=False)