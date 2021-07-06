from scrapperportaldaqueixa import getLinks, writeFile

brand = input('choose a brand:')

complaints = getLinks(brand)
writeFile(brand, complaints)
