# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import shutil


def scraping_book_description_and_img(dic_name_and_url):
    """
    fonction qui va créer un dossier par categorie, créer un fichier csv dans le dossier
    categorie avec les données de chaques book par categorie et un dossier img dans chaque dossier categorie
    avec les images et titres de chaque book par categorie.
    :param: le dictionnaire qui regroupe le nom des categories et les urls par categories
     """
    # pour chaque categories
    for key, values in dic_name_and_url.items():
        # creation des dossiers
        os.makedirs(key, exist_ok=True)
        os.makedirs("C:\\Users\\marie\\PycharmProjects\\projetOcr2\\" + key + "\\img", exist_ok=True)
        # creation des fichier csv
        with open(key + "/description_book_" + key + ".csv", 'w', encoding='utf-8') as file:
            # pour chaque urls dans la categorie on scrap et récup les données
            for url_book in values:
                url = url_book
                response = requests.get(url)
                if response.ok:
                    soup = BeautifulSoup(response.text, "html.parser")
                    title = soup.find('div', {'class': 'col-sm-6 product_main'}).find('h1')
                    description = soup.find('article', {'class': 'product_page'}).find_all('p')
                    image = soup.find('div', {'class': 'item active'}).find('img')
                    src = image['src']
                    name_image = image['alt']
                    # ici on enleve les caractères spéciaux
                    real_name_image = ''.join(e for e in name_image if e.isalnum())
                    base_url = "http://books.toscrape.com/"
                    url_image = urljoin(base_url, src)
                    # partie pour récup l'image et l'enregistrer dans le dossier img
                    responses = requests.get(url_image, stream=True)
                    if responses.ok:
                        files = open("C:\\Users\\marie\\PycharmProjects\\projetOcr2\\" + key + "\\img\\"
                                     + real_name_image + ".png", 'wb')
                        responses.raw.decode_content = True
                        shutil.copyfileobj(responses.raw, files)
                        del responses
                    list_book = soup.find("table", {"class": 'table-striped'}).find_all('td')
                    del response
                    # dictionnaire des données d'un book
                    dic_book = {'product_page_url': url,
                                'universal_product_code': list_book[0].text,
                                'category': list_book[1].text,
                                'title': title.text,
                                'product_description': description[3].text,
                                'price_including_tax': list_book[3].text,
                                'price_excluding_tax': list_book[2].text,
                                'number_available': list_book[5].text,
                                'review_rating': list_book[6].text,
                                'url_image': url_image
                                }
                # on ecrit les données du book dans le fichier csv             }
                for clef, valeurs in dic_book.items():
                    file.write(clef + ':' + valeurs + '\n')
                file.write('\n\n')
    file.close()
    files.close()


def scraping_book_by_categorie(urls_category):
    """
    fonction qui permet de récuperer les urls de tout les book par catégories
    :param: une list des urls des tte la categories
    :return:une list avec pour chaque list de categorie ses urls respectives(des listes dans une liste)
    """
    list_link_book = []
    list_link_book_by_category = []
    # on boucle sur chaque url categorie
    for url_category in urls_category:
        url = url_category
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            #on cherche si il ya un bouton next dans la page
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
                # tant qu'il ya un button next on recup l'url de la page suivante et on scrap la page
                # jusqu'a qu'il n'y ai plus de next (pagination)
                while button_next:
                    new_url = url[:-10]
                    # ici ca permet de voir si la condition de la boucle est bonne avec button_next
                    button_next = soup.find('li', {'class': 'next'}).find('a')
                    href = button_next['href']
                    # nouvelle page nouvelle url qu'on récup
                    url = urljoin(new_url, href)
                    response = requests.get(url)
                    if response.ok:
                        soup = BeautifulSoup(response.text, "html.parser")
                        urls_book = soup.findAll('div', {'class': 'image_container'})
                        del response
                        # on cherche tte les urls des book par page
                        for url_book in urls_book:
                            a = url_book.find('a')
                            link_book = a['href']
                            base_url = "http://books.toscrape.com"
                            real_link_book = urljoin(base_url, '/catalogue' + link_book[8:])
                            #on stock les urls des book dans un tableau
                            list_link_book.append(real_link_book)
            except:
                pass
            #on stock chaque tableau d'urls par categories
            list_link_book_by_category.append(list_link_book)
            #on vide la tableau des urls des book pour qu'a le prochaine categorie il soit vide
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
