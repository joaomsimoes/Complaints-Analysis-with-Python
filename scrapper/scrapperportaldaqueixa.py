from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql
import json
import textacy.preprocessing

f = open('gcp.json')
data = json.load(f)

conn = pymysql.connect(host=data['host'], user=data['user'], passwd=data['passwd'], db=data['db'])
cur = conn.cursor()


def get_links(brand, pagecount=None):

    create_table(brand)

    if not pagecount:
        html = urlopen('https://portaldaqueixa.com/brands/{}/complaints/'.format(brand))
        bs = BeautifulSoup(html, 'html.parser')
        pagination = bs.find_all("li", {"class": "page-item"})
        pagecount = int(pagination[(len(pagination) - 1)].find_all("a")[0].attrs['data-ci-pagination-page'])
  
    pages = set()
    complaints = []
    unwritten_complaints = []
    write_sql(brand, [])
    for page in range(pagecount):
        # open the html and start the soup
        html = urlopen('https://portaldaqueixa.com/brands/{}/complaints/?p={}'.format(brand, (page + 1)))
        bs = BeautifulSoup(html, 'html.parser')

        # find a new link and iterate it over
        for link in bs.find_all('a', href=re.compile('^(https://portaldaqueixa.com/brands/{}/complaints/{}.*)'.format(brand, brand))):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    new_page = link.attrs['href']
                    print('-'*20)
                    print(new_page)
                    pages.add(new_page)
                    complaint = get_info(brand, new_page)
                    complaints.append(complaint)
                    unwritten_complaints.append(complaint)
        if page % 2 == 0:
            write_sql(brand, unwritten_complaints)
            unwritten_complaints = []
    return complaints


def create_table(brand):
    cur.execute('USE scrapper')

    # Criar uma nova tabela para cada marca
    table = "CREATE TABLE IF NOT EXISTS {} (id BIGINT(7) NOT NULL AUTO_INCREMENT, \
        data TEXT, title TEXT, comment TEXT, \
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
        PRIMARY KEY(id))  \
        CHARACTER SET = latin1 COLLATE = latin1_general_ci".format(brand)

    cur.execute(table)
    conn.commit()


def close_db():
    cur.close()
    conn.close()


def get_info(brand, url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')

    date_find = bs.find("time")
    date_text = date_find.get_text()[1:]

    brand_title_find = bs.find('h4')
    brand_title_text = (brand_title_find.get_text())[len(brand)+3:]
    brand_title_text = normalize(brand_title_text)

    comentario_find = bs.find_all("div", class_='complaint-detail-body-description')
    comentario_text = ''.join([c.get_text(' ', strip=True).strip() for c in comentario_find])
    comentario_text = normalize(comentario_text)

    return date_text, brand_title_text, comentario_text


def normalize(text):
    text = textacy.preprocessing.remove.accents(text)
    return text


def write_sql(brand, complaints):
    insert = "INSERT INTO {} (data, title, comment) \
           VALUES (%s, %s, %s)".format(brand)
    for (date, title, comment) in complaints:
        try:
            cur.execute(insert, (date, title, comment))
            conn.commit()
        except:
            print('este nao deu')
