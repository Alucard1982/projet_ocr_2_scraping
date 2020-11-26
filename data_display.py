# coding: utf-8
import os
from tqdm import tqdm
import csv
import requests
from bs4 import BeautifulSoup
import shutil


def data_display_book(list_name_dic_book_by_categorie):
    """ "
    fonction d'affichage de tout les description de book ainsi que les images classées dans des dossiers
    """
    os.makedirs("data", exist_ok=True)
    for name_categorie, list_dic_book in list_name_dic_book_by_categorie:
        path = "C:\\Users\\marie\\PycharmProjects\\projetOcr2\\data\\" + name_categorie
        os.makedirs(path, exist_ok=True)
        os.makedirs(path + "\\img", exist_ok=True)
        file = open(path + "/description_book_" + name_categorie + ".csv", "w", encoding="utf-8")
        file.write(
            "product_page_url,universal_product_code,category,title,product_description,price_including_tax,"
            "price_excluding_tax,number_available,review_rating,url_image\n"
        )
        for dic_book in tqdm(list_dic_book):
            writer = csv.DictWriter(
                file,
                dic_book.keys(),
                dialect="excel",
                lineterminator="\n",
                quoting=csv.QUOTE_MINIMAL,
            )
            response = requests.get(dic_book["product_page_url"])
            soup = BeautifulSoup(response.text, "html.parser")
            if response.ok:
                image = soup.find("div", {"class": "item active"}).find("img")
                name_image = image["alt"]
                del response
                real_name_image = "".join(e for e in name_image if e.isalnum())
                responses = requests.get(dic_book["url_image"], stream=True)
                if responses.ok:
                    files = open(path + "\\img\\" + real_name_image + ".png", "wb")
                    responses.raw.decode_content = True
                    shutil.copyfileobj(responses.raw, files)
                    del responses
            writer.writerow(dic_book)
        file.close()
        files.close()


# on pourrait écrire une fonction avec matplotlib pour créer un graphique avec les données.Un graphique par exemple
# qui donnerait la moyenne des prix des book par categeorie.(more fun)
