# Projet 2 OpenClassrooms
## Books online: Les exigences du système de surveillance des prix

Ce script va permettre de scrapper le site https://books.toscrape.com/ .
Il va récupérer l'ensemble des informations suivantes:

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

Vous trouverez l'ensemble des données repertoriées par catégories de livres avec les couvertures correspondantes dans le dossier images.
Selon l'arboresence suivante :
```
-- datas
    -- categorie 1
        -- categorie 1.csv
        -- images
            -- image 1.jpg
            -- image 2.jpg
    -- categorie 2
        -- ...
```

### Installation:
Vous devez avoir préalablement Python installé ainsi qu'un IDE (PyCharm ou Virtual Studio)

Placez vous dans le répertoire souhaité puis clonez le repository:
```
git clone https://github.com/Antinii/Projet_2.git
```
Déplacez vous dans le dossier du repository avec:
```
cd '.\Projet_2\'
```
Créez votre environnement virtuel:
```
python -m venv env
```
Activez votre environnement virtuel:
```
env\Scripts\activate
```
Installez les packages nécessaires:
```
pip install -r requirements.txt
```
Et pour terminer, lancez le script:
```
python main.py
```

