# coding: utf-8
import requests
from bs4 import BeautifulSoup


def create_dict(list_link_book_by_category):
    """
    crée un dictionnaire pour associer le nom de la categories à ses urls respective
    :param list_link_book_by_category:
    :return: un dictionnaire avec comme clef le nom de la categories et valeur les url de la categorie
    """
    list_name_categorie = []
    name_and_url = {}
    url = "https://books.toscrape.com/index.html"
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        urls_category = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
        del response
        for url_category in urls_category:
            a = url_category.find('a')
            name_category = a.text.strip()
            list_name_categorie.append(name_category)
        for i in range(len(list_name_categorie)):
            name_and_url[list_name_categorie[i]] = list_link_book_by_category[i]

    return name_and_url
