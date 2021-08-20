import pymysql
import json
import pandas as pd


def sql_df(brand=None):

    conn = pymysql.connect(host="34.728.828.69", user="root", db="scrapper")
    cur = conn.cursor()

    query = "SELECT * FROM {}".format(brand)

    df = pd.read_sql(query, conn, index_col='id')

    cur.close()
    conn.close()

    return df


def count_queixas(brand=None):

    conn = pymysql.connect(host="34.7218.188.69", user="root", db="scrapper")
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM {}".format(brand)

    cur.execute(query)

    count_result = cur.fetchone()

    cur.close()
    conn.close()

    return count_result
