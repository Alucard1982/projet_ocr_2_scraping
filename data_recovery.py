# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scraping_book_description():
    """
    Fonction qui permet de récup les données d'un book
    """
    url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    #on recup l'url
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find('h1')
        description = soup.findAll('p')
        image = soup.find('img')
        src = image['src']
        base_url = "http://books.toscrape.com/"
        url_image = urljoin(base_url, src)
        list_book = soup.findAll('td')
        dic_book = {'product_page_url': url, 'universal_product_code': list_book[0].text,
                    'category': list_book[1].text,
                    'title': title.text, 'product_description': description[3].text,
                    'price_including_tax': list_book[3].text, 'price_excluding_tax': list_book[2].text,
                    'number_available': list_book[5].text, 'review_rating': list_book[6].text,
                    'url_image': url_image
                    }
        with open('description_book.csv', 'w', encoding='utf-8') as file:
            for key, values in dic_book.items():
                file.write(key + ':' + values + '\n')
                print(values)


def scraping_book_by_categorie(urls_category):
    """
    prend en parametre d'entrer une list des urls des tte la categories
    fonction qui permet de récuperer les urls de tout les book par catégories
    :return:une list avec pour chaque list de categorie ses urls respectives(des listes dans une liste)
    """
    list_link_book = []
    list_link_book_by_category = []
    #on boucle sur chaque categories
    for url_category in urls_category:
        url = url_category
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                button_next = soup.find('li', {'class': 'next'}).find('a')
            except:
                pass
            soup = BeautifulSoup(response.text, "html.parser")
            urls_book = soup.findAll('div', {'class': 'image_container'})
            del response
            for url_book in urls_book:
                a = url_book.find('a')
                link_book = a['href']
                base_url = "http://books.toscrape.com"
                real_link_book = urljoin(base_url, '/catalogue' + link_book[8:])
                list_link_book.append(real_link_book)
        try:
            # tant que qu'il ya un button next on recup l'url de la page suivante et on scrap la page
            # jusqu'a qu'il n'y ai plus de next (pagination)
            while button_next:
                new_url = url[:-10]
                button_next = soup.find('li', {'class': 'next'}).find('a')
                href = button_next['href']
                url = urljoin(new_url, href)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                urls_book = soup.findAll('div', {'class': 'image_container'})
                del response
                #on cherche tte les urls de book par page
                for url_book in urls_book:
                    a = url_book.find('a')
                    link_book = a['href']
                    base_url = "http://books.toscrape.com"
                    real_link_book = urljoin(base_url, '/catalogue' + link_book[8:])
                    list_link_book.append(real_link_book)
        except:
            pass
        list_link_book_by_category.append(list_link_book)
        list_link_book = []

    return list_link_book_by_category


def scraping_category():
    """
    fonction qui permet de récuperer toutes les urls des catégories
    :return:la list des urls de toutes les categories
    """

    list_link_categorie = []
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        urls_category = soup.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
        del response
        for url_category in urls_category:
            a = url_category.find('a')
            link_category = a['href']
            base_url = "http://books.toscrape.com"
            real_link_category = urljoin(base_url, link_category)
            list_link_categorie.append(real_link_category)
    return list_link_categorie
