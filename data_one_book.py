import requests
import csv
from bs4 import BeautifulSoup

# PHASE 1
# Scraping des données demandées pour l'ouvrage selectionné

# Fonction pour extraire les données d'un seul livre


def data_one_book(url_book):
    response = requests.get(url_book)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
        td = soup.find_all('td')
        upc = td[0].get_text()
        price_excluding_taxes = td[2].get_text()
        price_including_taxes = td[3].get_text()
        stock = td[5].get_text()
        description = soup.find('div', {'id': 'product_description'})
        if description is not None:
            description = description.find_next_sibling().text
        else:
            description = 'No description'
        category = soup.find('li', {'class': 'active'}).find_previous('li')
        rating = soup.find('i', {'class': 'icon-star'}).find_parent('p').get('class')
        find_img_url = soup.find('div', {'class': 'item active'}).find('img').attrs['src']
        img_url = 'https://books.toscrape.com/'+find_img_url.replace("../../", "")
        data = {
            'url page': url_book,
            'upc': upc,
            'title': title.text,
            'price with taxes': price_including_taxes,
            'price without taxes': price_excluding_taxes,
            'stock': stock,
            'description': description,
            'category': category.text.strip(),
            'rating reviews': (rating[1].lower() + ' out of five'),
            'image url': img_url
        }
        return data

    # Fonction print permettant l'extraction des données scrapés vers un fichier CSV
    def print_csvs(data_list, file_name):
        headers = ['url page', 'upc', 'title', 'price with taxes', 'price without taxes', 'stock', 'description',
                   'category', 'rating reviews', 'image url']
        with open(file_name, 'w', newline='', encoding='utf8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_list)

    # Fin de la phase 1 : extraction des données du livre Dune vers fichier CSV
    url_dune = 'https://books.toscrape.com/catalogue/dune-dune-1_151/'
    book = data_one_book(url_dune)
    print_csvs([book], 'dune_book.csv')
