import requests
from bs4 import BeautifulSoup
from data_one_book import data_one_book
from data_one_book import print_csvs


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


# Creation d'un fichier sf_books.csv contenant les données de tous les livres de la catégorie science fiction


url_cat_sf = 'https://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html'
cat = get_all_links_book(url_cat_sf)
data_sf_print = []
for datas_books in cat:
    datas_list_books = data_one_book(datas_books)
    data_sf_print.append(datas_list_books)
print_csvs(data_sf_print, 'sf_books.csv')
