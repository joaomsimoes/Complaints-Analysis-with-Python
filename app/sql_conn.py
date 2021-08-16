import pymysql
import json
import pandas as pd

def sql_df(brand=None):
    f = open('gcp.json')
    data = json.load(f)

    conn = pymysql.connect(host=data['host'], user=data['user'], passwd=data['passwd'], db=data['db'])
    cur = conn.cursor()

    query = "SELECT * FROM {}".format(brand)

    df = pd.read_sql(query, conn,index_col='id')

    cur.close()
    conn.close()

    return df

def count_queixas(brand=None):
    f = open('gcp.json')
    data = json.load(f)

    conn = pymysql.connect(host=data['host'], user=data['user'], passwd=data['passwd'], db=data['db'])
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM {}".format(brand)

    cur.execute(query)

    count_result = cur.fetchone()

    cur.close()
    conn.close()

    return count_result