from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re
import sys
sys.setrecursionlimit(10000)

pages = set()
dictf = {}

def getLinks(brand):
  ''' Portal da Queixa WebScrapper. It scrappes only the ../{brand}/complaint/* pages
  Arguments>
    brand: choose the brand name from the link, ex. "uber-eats"
  Return:
    CSV file with the name of the brand and for each row complain title and its text'''
  
  global pages, dictf

  # open the html and start the soup 
  html = urlopen('https://portaldaqueixa.com/brands/{}/complaints/'.format(brand))
  bs = BeautifulSoup(html, 'html.parser')

  # get the title and complaint text from the page 
  lenght_brand = len(str(brand))

  brand_title_find = bs.find('h4')
  brand_title_text = brand_title_find.get_text()

  comentario_find = bs.find_all("div", class_='complaint-detail-body-description')
  comentario_text = [c.get_text(' ', strip=True).strip() for c in comentario_find]

  dictf[brand_title_text[lenght_brand+3:]] = ''.join(comentario_text)

  # saves all the complaints to a csv file
  with open('{}.csv'.format(brand), 'w+', encoding='latin-1', errors='replace') as a_file:
    writer = csv.writer(a_file)
    for key, value in dictf.items():
      writer.writerow([key, value])

  # find a new link and iterate it over
  for link in bs.find_all('a', href=re.compile('^(https://portaldaqueixa.com/brands/{}/complaints/{}.*)'.format(brand, brand))):
    if 'href' in link.attrs:
      if link.attrs['href'] not in pages:
        newPage = link.attrs['href']
        print('-'*20)
        print(newPage)
        pages.add(newPage)
        getLinks(brand)
