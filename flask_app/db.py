"""
@author kingfish
db访问
"""
import pymysql
import pprint

def get_conn():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='root',
        database='kingfish',
        charset='utf8'
    )

def query_data(sql):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data
    finally:
        conn.close()
        
def insert_or_update(sql):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
    finally:
        conn.close()
        
if __name__ == "__main__":
    #插入一条数据
    insert_sql = "insert into user(name,sex,age,email) values('小王','男',30,'xiaoyuge@gmail.com')"
    insert_or_update(insert_sql)
    #查询数据
    query_sql = 'select * from user'
    data = query_data(query_sql)
    pprint.pprint(data)

    
