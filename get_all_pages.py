import requests
from data_one_book import print_csvs
from data_one_book import data_one_book
from get_all_links_book import get_all_links_book
from bs4 import BeautifulSoup

# Fonction permettant d'obtenir toutes les pages d'une catégorie de livres (gestion pagination)


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


url_cat_defaut = 'https://books.toscrape.com/catalogue/category/books/default_15/index.html'
links_cat_defaut = get_all_pages(url_cat_defaut)
data_cat_defaut = []
for links_cat in links_cat_defaut:
    all_defaut_links = get_all_links_book(links_cat)
    for defaut_book_data in all_defaut_links:
        all_book_data = data_one_book(defaut_book_data)
        data_cat_defaut.append(all_book_data)
print_csvs(data_cat_defaut, 'categorie defaut.csv')

# Fin de la phase 2 : extraction des données d'une catégorie (defaut) avec plus d'une page vers fichier CSV
