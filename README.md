# Projet 2 OpenClassrooms
## Books online: Les exigences du système de surveillance des prix

# Installation:
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
env\Scripts\activate.bat
```
Installez les packages nécessaires:
```
pip install -r requirements.txt
```
Et pour terminer, lancez le script:
```
python main.py
```
Le script va scrapper le site https://books.toscrape.com/ afin de récupérer les données nécessaires.
Vous trouverez l'ensemble des données répertoriées par catégories de livres avec les couvertures correspondantes dans le dossier images.
