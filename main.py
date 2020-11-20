# coding: utf-8
import data_recovery as data
import grouping_data as dic_data


def main():
    #on récup les urls des categories
    url_categorie = data.scraping_category()
    #on récup les urls des book pour chaque categories
    url_book_by_categorie = data.scraping_book_by_categorie(url_categorie)
    #on regroupe les données dans un dictionnaire
    dic_name_url = dic_data.create_dict(url_book_by_categorie)
    #on affiche les données de chaque book ainsi que leurs images
    data.scraping_book_description_and_img(dic_name_url)


if __name__ == '__main__':
    main()
