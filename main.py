from data_one_book import data_one_book
from get_all_links_book import get_all_links_book
from get_all_pages import get_all_pages
from get_all_cat import get_all_cat

import os
import csv
import requests


main_url = 'https://books.toscrape.com/'
all_category = get_all_cat(main_url)  # Extraction des liens de toutes les catégories.
datas = os.path.join(os.path.dirname(__file__), 'datas')  # Définition du répertoire de travail

if not os.path.exists(datas):  # Création du dossier datas s'il n'existe pas deja
    os.mkdir(datas)
for cat in all_category:  # Pour chaque catégories du site
    books_category = []  # Liste des livres de la catégorie vide
    links_category = get_all_pages(cat['category_url'])  # Obtenir tous les liens des différents pages catégories
    for all_links_books in links_category:  # Pour chaque page de la catégory
        all_books = get_all_links_book(all_links_books)  # Obtenir tous les liens des livres de la page links_category
        for book in all_books:  # Pour chaque livre dans tous les livres de la catégorie
            data_book = data_one_book(book)  # Obtenir toutes les données de chaque book
            books_category.append(data_book)  # Les ajouter à la liste des livres de la catégorie

    category_path = f"datas/{cat['category_name']}"  # Chemin de création des dossiers de catégorie
    if not os.path.exists(category_path):
        os.makedirs(category_path)  # Création des dossiers par nom de catégorie
    headers = ['url page', 'upc', 'title', 'price with taxes', 'price without taxes', 'stock', 'description',
               'category', 'rating reviews', 'image url']
    # Création d'un fichier CSV par catégories dans le dossier datas.
    with open(os.path.join(category_path, f"{cat['category_name']}.csv"), 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for one_book in books_category:  # Pour chaque livre dans tous les livres de la catégorie
            writer.writerow(one_book)  # Ecrire une ligne dans le fichier CSV
            books_category = []  # retourner liste vide en fin de boucle sinon les anciennes catégories s'y ajoutent

            # PHASE 4
            # Téléchargement des images de chaque livres.

            images_path = f"datas/{cat['category_name']}/images"  # Définition de l'emplacement  du dossier images
            if not os.path.exists(images_path):
                os.mkdir(images_path)  # Création du dossier images dans chaque dossier de catégories
            response = requests.get(f"{one_book['image url']}")  # Récupérer l'url de l'image
            with open(os.path.join(images_path, f"{cat['category_name']}, {one_book['upc']}.jpg"), 'wb') as f:
                f.write(response.content)  # Télécharger l'image du livre dans le dossier images
