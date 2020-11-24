# coding: utf-8
import data_recovery as data
import grouping_data
import data_display as display


def main():

    url_categorie = data.scraping_category()
    url_book_by_categorie = data.scraping_book_by_categorie(url_categorie)
    dic_name_url = grouping_data.create_dict(url_book_by_categorie)
    dic_data_name_url_by_categorie = data.scraping_book_description(dic_name_url)
    display.data_display_book(dic_data_name_url_by_categorie)


if __name__ == "__main__":
    main()
