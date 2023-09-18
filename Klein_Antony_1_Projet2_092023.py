# Import des packets nécessaires
import csv
import os
import requests
from bs4 import BeautifulSoup










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
    list_all_pages = [url_category]
    base_url = url_category[:-10]
    while True:
        response = requests.get(url_category)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            have_pagination = soup.find('li', {'class': 'next'})
            if have_pagination is not None:
                next_page = have_pagination.find('a')['href']
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
'''
url_cat_defaut = 'https://books.toscrape.com/catalogue/category/books/default_15/index.html'
links_cat_defaut = get_all_pages(url_cat_defaut)
data_cat_defaut = []
for links_cat in links_cat_defaut:
    all_defaut_links = get_all_links_book(links_cat)
    for defaut_book_data in all_defaut_links:
        all_book_data = data_one_book(defaut_book_data)
        data_cat_defaut.append(all_book_data)
print_csvs(data_cat_defaut, 'categorie defaut.csv')
'''

# PHASE 3
# Fonction permettant l'extraction de tous les liens des catégories du site


def get_all_cat(url):
    all_cat_links = []
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        find_cat_links = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
        for lis in find_cat_links:
            a = lis.find('a')
            cat_links = a['href']
            link = url + cat_links
            cat_name = a.text.strip().lower()
            all_cat_links.append(
                {
                    'category_url': link,
                    'category_name': cat_name
                }
            )
        return all_cat_links


main_url = 'https://books.toscrape.com/'
all_cat = get_all_cat(main_url)
datas = os.path.join(os.path.dirname(__file__), 'datas')
all_book_datas = []
if not os.path.exists(datas):
    os.mkdir(datas)
for cats in all_cat:
    links_cat = get_all_pages(cats['category_url'])
    for all_links_books in links_cat:
        all_books = get_all_links_book(all_links_books)
        for books in all_books:
            data_books = data_one_book(books)
            all_book_datas.append(data_books)

    headers = ['url page', 'upc', 'title', 'price with taxes', 'price without taxes', 'stock', 'description',
               'category', 'rating reviews', 'image url']
    with open(os.path.join(datas, f"{cats['category_name']}.csv"), 'w', newline='', encoding='utf8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for one_book in all_book_datas:
            writer.writerow(one_book)
    all_book_datas = []  # retourner liste vide à la fin de la boucle sinon les anciennes catégories s'y ajoutent
