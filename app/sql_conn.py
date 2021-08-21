import sqlalchemy
import json
import pandas as pd

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

# https://cloud.google.com/sql/docs/mysql/connect-run - Connect Cloud Run to Cloud SQL
pool = sqlalchemy.create_engine(
    # Equivalent URL:
    # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
    sqlalchemy.engine.url.URL.create(
        drivername="mysql+pymysql",
        username=db_user,  # e.g. "my-database-user"
        password=db_pass,  # e.g. "my-database-password"
        database=db_name,  # e.g. "my-database-name"
        query={"unix_socket": "/cloudsql/{}/".format(cloud_sql_connection_name)}),
    **db_config
)

def sql_df(brand=None, pool=pool):

    conn = pool.connect()
    cur = conn.cursor()

    query = "SELECT * FROM {}".format(brand)

    df = pd.read_sql(query, conn, index_col='id')

    cur.close()
    conn.close()

    return df


def count_queixas(brand=None, pool=pool):

    conn = pool.connect()
    cur = conn.cursor()

    query = "SELECT COUNT(*) FROM {}".format(brand)

    cur.execute(query)

    count_result = cur.fetchone()

    cur.close()
    conn.close()

    return count_result