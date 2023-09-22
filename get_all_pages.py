import requests
from data_one_book import print_csvs
from data_one_book import data_one_book
from get_all_links_book import get_all_links_book
from bs4 import BeautifulSoup

# Fonction permettant d'obtenir toutes les pages d'une catégorie de livres (gestion pagination)


def get_all_pages(url_category):
    list_all_pages = [url_category]
    base_url = url_category[:-10]  # Obtenir le lien sans les 10 derniers caractères
    while True:
        response = requests.get(url_category)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            have_pagination = soup.find('li', {'class': 'next'})  # Chercher bouton next sur la page
            if have_pagination is not None:  # Si bouton next existe
                next_page = have_pagination.find('a')['href']  # chercher le lien du bouton next
                next_page = base_url + next_page  # concaténer le lien de base avec le lien du bouton next
                list_all_pages.append(next_page)  # les ajouter à la liste de toutes les pages
                url_category = next_page  # redémarrer la boucle à la page next
            else:
                return list_all_pages


# Extraction des données d'une catégorie (defaut) avec plus d'une page vers fichier CSV


url_cat_default = 'https://books.toscrape.com/catalogue/category/books/default_15/index.html'
links_cat_default = get_all_pages(url_cat_default)
data_cat_default = []
for links_cat in links_cat_default:
    all_default_links = get_all_links_book(links_cat)
    for default_book_data in all_default_links:
        all_book_data = data_one_book(default_book_data)
        data_cat_default.append(all_book_data)
print_csvs(data_cat_default, 'category_default.csv')

# Fin de la phase 2
