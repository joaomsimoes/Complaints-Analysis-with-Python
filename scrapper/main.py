import time
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import argparse
from db import *

parser = argparse.ArgumentParser()
parser.add_argument("brand", type=str)
args = parser.parse_args()


def get_comments(brand=None):
    create_table(brand, 'comments')
    all_links = set(get_all_links(brand))

    for link in all_links:
        time.sleep(2)
        complaint = get_info(brand, link)
        write_sql(brand, complaint, link)
        update_link(brand, link)
        print('-' * 20)
        print(link)


def get_links(brand):
    create_table(brand, 'links')

    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    url = f'https://portaldaqueixa.com/brands/{brand}/complaints/'
    req = urllib.request.Request(url, headers=hdr)
    html = urlopen(req, timeout=5)

    bs = BeautifulSoup(html, 'html.parser')
    pagination = bs.find_all("li", {"class": "page-item"})
    pagecount = int(pagination[(len(pagination) - 1)].find_all("a")[0].attrs['data-ci-pagination-page'])

    last_page = check_last_page(brand)

    for page in range(last_page, pagecount):
        page = page + 1
        time.sleep(2)
        # open the html and start the soup
        html = urlopen(f'https://portaldaqueixa.com/brands/{brand}/complaints/?p={page}')
        bs = BeautifulSoup(html, 'html.parser')

        # find a new link and iterate it over
        for link in bs.find_all('a', href=re.compile(f'^(https://portaldaqueixa.com/brands/{brand}/complaints/{brand}.*)')):
            if 'href' in link.attrs:
                new_page = link.attrs['href']
                print(new_page)
                links_to_db(brand, new_page, page)


def get_info(brand, url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(url, headers=hdr)
    html = urlopen(req)
    bs = BeautifulSoup(html, 'html.parser')

    date_find = bs.find("time")
    date_text = date_find.get_text()[1:]

    brand_title_find = bs.find('h4')
    brand_title_text = (brand_title_find.get_text())[len(brand)+3:]

    comentario_find = bs.find_all("div", class_='complaint-detail-body-description')
    comentario_text = ''.join([c.get_text(' ', strip=True).strip() for c in comentario_find])

    return date_text, brand_title_text, comentario_text


if __name__ == '__main__':
    brand = args.brand
    get_links(brand)
    get_comments(brand)
