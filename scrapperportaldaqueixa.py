from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import re
import sys
sys.setrecursionlimit(10000)

def getLinks(brand, pageCount = None):
  ''' Portal da Queixa WebScrapper. It scrappes only the ../{brand}/complaint/* pages
  Arguments>
    brand: choose the brand name from the link, ex. "uber-eats"
  Return:
    CSV file with the name of the brand and for each row complain title and its text'''

  if not pageCount:
    html = urlopen('https://portaldaqueixa.com/brands/{}/complaints/'.format(brand))
    bs = BeautifulSoup(html, 'html.parser')
    pagination = bs.find_all("li", {"class": "page-item"})
    pageCount = int(pagination[(len(pagination) - 1)].find_all("a")[0].attrs['data-ci-pagination-page'])
  
  pages = set()
  complaints = []
  unwrittenComplaints = []
  writeFile(brand, [], False, True)
  for page in range(pageCount):
    # open the html and start the soup 
    html = urlopen('https://portaldaqueixa.com/brands/{}/complaints/?p={}'.format(brand, (page + 1)))
    bs = BeautifulSoup(html, 'html.parser')

    # find a new link and iterate it over
    for link in bs.find_all('a', href=re.compile('^(https://portaldaqueixa.com/brands/{}/complaints/{}.*)'.format(brand, brand))):
      if 'href' in link.attrs:
        if link.attrs['href'] not in pages:
          newPage = link.attrs['href']
          print('-'*20)
          print(newPage)
          pages.add(newPage)
          complaint = getInfo(brand, newPage)
          complaints.append(complaint)
          unwrittenComplaints.append(complaint)
    if page % 2 == 0:
      writeFile(brand, unwrittenComplaints, True, False)
      unwrittenComplaints = []
  return complaints

def getInfo(brand, url):
  html = urlopen(url)
  bs = BeautifulSoup(html, 'html.parser')

  brand_title_find = bs.find('h4')
  brand_title_text = (brand_title_find.get_text())[len(brand)+3:]

  comentario_find = bs.find_all("div", class_='complaint-detail-body-description')
  comentario_text = ''.join([c.get_text(' ', strip=True).strip() for c in comentario_find])

  return (brand_title_text, comentario_text)

def writeFile(brand, complaints, append = False, header = True):
  writeType = "a" if append else "w+"
  with open('{}.csv'.format(brand), writeType, encoding='latin-1', errors='replace') as a_file:
    # saves all the complaints to a csv file
    writer = csv.writer(a_file)
    if header:
      writer.writerow(['title', 'comment'])
    for (title, comment) in complaints:
      writer.writerow([title, comment])
