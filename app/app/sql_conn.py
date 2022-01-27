import sqlalchemy
import json
import pandas as pd

f = open('db.json')
data = json.load(f)


def init_db_connection():
    engine = sqlalchemy.create_engine(data['connection'])

    return engine


def sql_df(brand=None):
    engine = init_db_connection()
    with engine.connect() as conn:
        query = "SELECT * FROM {}".format(brand)
        df = pd.read_sql(query, conn, index_col=None)

    return df


def brands():
    engine = init_db_connection()
    with engine.connect() as conn:
        query = "SHOW TABLES WHERE `Tables_in_portaldaqueixa` NOT LIKE '%%_links'"
        query_result = conn.execute(query)
        query_result = query_result.fetchall()

    brands_list = [i[0] for i in query_result]

    return brands_list
