# Import des packets nécessaires
import csv
import requests
from bs4 import BeautifulSoup

# PHASE 1
url_dune = 'https://books.toscrape.com/catalogue/dune-dune-1_151/'
response = requests.get(url_dune)

# Scraping des données demandées pour l'ouvrage selectionné
headers = ['url page', 'upc', 'titre', 'prix avec taxes', 'prix sans taxes', 'quantité en stock', 'description',
           'catégorie', 'note avis', 'url image']
dune_book = []
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
    td = soup.find_all('td')
    upc = td[0].get_text()
    price_excluding_taxes = td[2].get_text()
    price_including_taxes = td[3].get_text()
    stock = td[5].get_text()
    description = soup.find('article', {'class': 'product_page'}).find_all('p')
    category = soup.find('li', {'class': 'active'}).find_previous('li')
    rating = soup.find('i', {'class': 'icon-star'}).find_parent('p').get('class')
    find_img_url = soup.find('div', {'class': 'item active'}).find('img').attrs['src']
    img_url = 'https://books.toscrape.com/'+find_img_url.replace("../../", "")
    data = {
        'url page': url_dune,
        'upc': upc,
        'titre': title.text,
        'prix avec taxes': price_including_taxes,
        'prix sans taxes': price_excluding_taxes,
        'quantité en stock': stock,
        'description': description[3].text,
        'catégorie': category.text.strip(),
        'note avis': (rating[1].lower() + ' out of five'),
        'url image': img_url
    }
    dune_book.append(data)

# Extraction des données vers fichier CSV
with open('dune_book.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(dune_book)


# PHASE 2
# Extraction des url de la catégorie science fiction
url_category = 'https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html'
response = requests.get(url_category)

if response.ok:
    cat_links = []
    soup = BeautifulSoup(response.text, 'html.parser')
    all_links = soup.find_all('h3')
    for h3 in all_links:
        a = h3.find('a')
        link = 'https://books.toscrape.com/catalogue/' + a['href'].replace('../../../', '')
        cat_links.append(link)
