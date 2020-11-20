# coding: utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scraping_book_description():
    url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
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


def scraping_book_by_categorie():
    list_link_book = []
    list_link_book_by_category = []

    url = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
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
            while button_next:
                new_url = url[:-10]
                button_next = soup.find('li', {'class': 'next'}).find('a')
                href = button_next['href']
                url = urljoin(new_url, href)
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                urls_book = soup.findAll('div', {'class': 'image_container'})
                del response
                for url_book in urls_book:
                    a = url_book.find('a')
                    link_book = a['href']
                    base_url = "http://books.toscrape.com"
                    real_link_book = urljoin(base_url, '/catalogue' + link_book[8:])
                    list_link_book.append(real_link_book)
        except:
            pass
        list_link_book_by_category.append(list_link_book)
        print(list_link_book_by_category)


