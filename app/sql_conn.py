import sqlalchemy
import json
import pandas as pd
import os

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]


# https://cloud.google.com/sql/docs/mysql/connect-run - Connect Cloud Run to Cloud SQL
def init_db_connection():
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={"unix_socket": "/cloudsql/{}".format(cloud_sql_connection_name)}))

    return pool


db = init_db_connection()


def sql_df(brand=None, pool=db):

    conn = pool.connect()
    cur = conn.cursor()

    query = "SELECT * FROM {}".format(brand)

    df = pd.read_sql(query, conn, index_col='id')

    cur.close()
    conn.close()

    return df


def count_queixas(brand=None, pool=db):

    conn = pool.connect()
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM {}".format(brand)

    cur.execute(query)

    count_result = cur.fetchone()

    cur.close()
    conn.close()

    return count_result
