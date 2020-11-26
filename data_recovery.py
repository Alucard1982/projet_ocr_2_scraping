# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm


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
        urls_category = (
            soup.find("ul", {"class": "nav nav-list"}).find("ul").find_all("li")
        )
        del response
        for url_category in urls_category:
            a = url_category.find("a")
            link_category = a["href"]
            base_url = "http://books.toscrape.com"
            real_link_category = urljoin(base_url, link_category)
            list_link_categorie.append(real_link_category)
    return list_link_categorie


def url_book(urls_book, list_link_book):
    for url_book in urls_book:
        a = url_book.find("a")
        link_book = a["href"]
        base_url = "http://books.toscrape.com"
        real_link_book = urljoin(base_url, "/catalogue" + link_book[8:])
        list_link_book.append(real_link_book)


def scraping_book_by_categorie(urls_category):
    """
    fonction qui permet de récuperer les urls de tout les book par catégories
    :param: une list des urls des tte la categories
    :return:une list avec pour chaque list de categorie ses urls respectives(des listes dans une liste)
    """
    list_link_book = []
    list_link_book_by_category = []
    for url_category in urls_category:
        url = url_category
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                button_next = soup.find("li", {"class": "next"}).find("a")
            except:
                pass
            soup = BeautifulSoup(response.text, "html.parser")
            urls_book = soup.findAll("div", {"class": "image_container"})
            del response
            url_book(urls_book, list_link_book)
            try:
                while button_next:
                    new_url = url[:-10]
                    button_next = soup.find("li", {"class": "next"}).find("a")
                    href = button_next["href"]
                    url = urljoin(new_url, href)
                    response = requests.get(url)
                    if response.ok:
                        soup = BeautifulSoup(response.text, "html.parser")
                        urls_book = soup.findAll("div", {"class": "image_container"})
                        del response
                        url_book(urls_book, list_link_book)
            except:
                pass
            list_link_book_by_category.append(list_link_book)
            list_link_book = []
    return list_link_book_by_category


def scraping_book_description(list_link_book_by_category):
    """
    foncion qui premet de récuperer un list de tuple avec pour chaque tuple le nom de la categorie et une liste de
    dictionnaire de la description de chaque book par categorie
    :param: le dictionnaire qui regroupe le nom des categories et les urls par categories
    :return: une liste de tuple
    """
    list_dic_book = []
    list_name_dic_book_by_categorie = []
    for list_urls_book in tqdm(list_link_book_by_category):
        for url_book in list_urls_book:
            url = url_book
            response = requests.get(url)
            if response.ok:
                soup = BeautifulSoup(response.text, "html.parser")
                title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1")
                description = soup.find("article", {"class": "product_page"}).find_all("p")
                list_p = soup.find("div", {"class": "col-sm-6 product_main"}).find_all("p")
                nb_stars = list_p[2]["class"]
                list_li = soup.find("ul", {"class": "breadcrumb"}).find_all("li")
                name_categorie = list_li[2].text.strip()
                image = soup.find("div", {"class": "item active"}).find("img")
                src = image["src"]
                base_url = "http://books.toscrape.com/"
                url_image = urljoin(base_url, src)
                list_book = soup.find("table", {"class": "table-striped"}).find_all("td")
                del response
                dic_book = {
                    "product_page_url": url,
                    "universal_product_code": list_book[0].text,
                    "category": name_categorie,
                    "title": title.text,
                    "product_description": description[3].text,
                    "price_including_tax": list_book[3].text,
                    "price_excluding_tax": list_book[2].text,
                    "number_available": list_book[5].text,
                    "review_rating": nb_stars[1] + "-Stars",
                    "url_image": url_image,
                }
                list_dic_book.append(dic_book)
        list_name_dic_book_by_categorie.append((name_categorie, list_dic_book))
        list_dic_book = []
    return list_name_dic_book_by_categorie
