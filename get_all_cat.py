from bs4 import BeautifulSoup
import requests


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
