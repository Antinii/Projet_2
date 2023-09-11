# Import des packets nécessaires
import csv
import requests
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/dune-dune-1_151/'
response = requests.get(url)

dune_book = []
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
    p = soup.find_all('p')
    td = soup.find_all('td')
    upc = td[0].get_text()
    price_excluding_taxes = td[2].get_text()
    price_including_taxes = td[3].get_text()
    stock = td[5].get_text()
    description = p[3].get_text()
    reviews = td[6].get_text()
    find_img_url = soup.find('div', {'class': 'item active'}).find('img').attrs['src']
    img_url = 'https://books.toscrape.com/'+find_img_url.replace("../../", "")
    data = {
        'url': url,
        'upc': upc,
        'titre': title.text,
        'prix sans taxes': price_excluding_taxes,
        'prix avec taxes': price_including_taxes,
        'stock': stock,
        'description': description,
        'nombre avis': reviews,
        'lien de l image': img_url
    }
    dune_book.append(data)

print(dune_book)
