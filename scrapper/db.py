import pymysql
import json

f = open('db.json')
data = json.load(f)
conn = pymysql.connect(host=data['host'], user=data['user'], passwd=data['pass'], db=data['db'])
cur = conn.cursor()


def create_table(brand, type):
    brand = brand.replace('-', '')
    if type == 'links':
        table_name = brand + '_links'
        links = f'CREATE TABLE IF NOT EXISTS {table_name} (id BIGINT(7) NOT NULL AUTO_INCREMENT,' \
                f'link TEXT, page INT, done INT, PRIMARY KEY(id))'

        cur.execute(links)
        conn.commit()

    if type == 'comments':
    # Criar uma nova tabela para cada marca
        table = f'CREATE TABLE IF NOT EXISTS {brand} (id BIGINT(7) NOT NULL AUTO_INCREMENT, \
            data TEXT, title TEXT, comment TEXT, link TEXT, \
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
            PRIMARY KEY(id))  \
            CHARACTER SET = latin1 COLLATE = latin1_general_ci'

        cur.execute(table)
        conn.commit()


def links_to_db(brand, link, page):
    brand = brand.replace('-', '')
    table_name = brand + '_links'
    links = f"INSERT INTO {table_name} (link, page, done) \
           VALUES (%s, %s, %s)"
    values = (link, page, 0)
    cur.execute(links, values)
    conn.commit()


def check_last_page(brand):
    brand = brand.replace('-', '')
    table_name = brand + '_links'
    query = f'SELECT page FROM {table_name} ORDER BY page DESC LIMIT 1'
    cur.execute(query)
    result = cur.fetchone()

    result = 0 if result is None else result[0]

    return result


def get_all_links(brand):
    brand = brand.replace('-', '')
    table_name = brand + '_links'
    query = f'SELECT link FROM {table_name} ' \
            f'WHERE done = 0'
    cur.execute(query)
    result = cur.fetchall()
    links = [link[0] for link in result]

    return links


def update_link(brand, link):
    brand = brand.replace('-', '')
    table_name = brand + '_links'
    query = f'UPDATE {table_name} SET done = 1 ' \
            f'WHERE link = "{link}"'
    cur.execute(query)


def close_db():
    cur.close()
    conn.close()


def write_sql(brand, complaints, link):
    brand = brand.replace('-', '')
    insert = f"INSERT INTO {brand} (data, title, comment, link) \
           VALUES (%s, %s, %s, %s)"
    date, title, comment = complaints
    try:
        cur.execute(insert, (date, title, comment, link))
        conn.commit()
    except:
        print('este nao deu')