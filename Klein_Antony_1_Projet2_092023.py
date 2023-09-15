# Import des packets nécessaires
import csv
import requests
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


# PHASE 2
# Extraction des liens des livres d'une catégorie selectionnée


# Fonction permettant l'extraction de tous les liens des livres d'une catégorie


def get_all_links_book(url_cat):
    response = requests.get(url_cat)
    links_cat_list = []
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('h3')
        for h3 in all_links:
            a = h3.find('a')
            link = 'https://books.toscrape.com/catalogue/' + a['href'].replace('../../../', '')
            links_cat_list.append(link)
        return links_cat_list

# Fonction permettant d'obtenir toutes les pages de la catégorie avec gestion de la pagination


def get_all_pages(url_category):
    list_all_pages = []
    list_all_pages.append(url_category)
    base_url = url_category[:-10]
    while True:
        response = requests.get(url_category)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            next = soup.find('li', {'class': 'next'})
            if next is not None:
                next_page = next.find('a')['href']
                next_page = base_url + next_page
                list_all_pages.append(next_page)
                url_category = next_page
            else:
                return list_all_pages


# Creation d'un fichier sf_books.csv contenant les données de tous les livres de la catégorie science fiction

url_cat_sf = 'https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html'
cat = get_all_links_book(url_cat_sf)
data_sf_print = []
for datas_books in cat:
    datas_list_books = data_one_book(datas_books)
    data_sf_print.append(datas_list_books)
print_csvs(data_sf_print, 'sf_books.csv')

# Fin de la phase 2 : extraction des données d'une catégorie (defaut) avec plus d'une page vers fichier CSV

url_cat_defaut = 'https://books.toscrape.com/catalogue/category/books/default_15/index.html'
links_cat_defaut = get_all_pages(url_cat_defaut)
data_cat_defaut = []
for links_cat in links_cat_defaut:
    all_defaut_links = get_all_links_book(links_cat)
    for defaut_book_data in all_defaut_links:
        all_book_data = data_one_book(defaut_book_data)
        data_cat_defaut.append(all_book_data)
print_csvs(data_cat_defaut, 'categorie defaut.csv')


# PHASE 3
# Fonction permettant l'extraction de tous les liens des catégories du site


def get_all_cat(url):
    url = 'https://books.toscrape.com/'
    all_cat_links = []
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        find_cat_links = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
        for lis in find_cat_links:
            a = lis.find('a')
            cat_links = a['href']
            link = url + cat_links
            all_cat_links.append(link)

        return all_cat_links


main_url = 'https://books.toscrape.com/index.html'
all_cat = get_all_cat(main_url)
for cats in all_cat:
    links_cat = get_all_pages(cats)
    for all_links_books in links_cat:
        all_books = get_all_links_book(all_links_books)
        for books in all_books:
            data_books = data_one_book(books)
            print(data_books)
