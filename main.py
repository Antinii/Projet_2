from data_one_book import data_one_book
from get_all_links_book import get_all_links_book
from get_all_pages import get_all_pages
from get_all_cat import get_all_cat

import os
import csv


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
