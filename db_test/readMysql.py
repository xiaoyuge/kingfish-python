"""
@author kingfish
读取mysql表数据
"""

import pymysql as pms
import pandas as pd

conn = pms.connect(host='localhost',
    user='root',
    password='mse2003219419',
    database='kingfish',
    charset='utf8'
    )

mysql_page = pd.read_sql("select * from titles",conn)

print(mysql_page)



