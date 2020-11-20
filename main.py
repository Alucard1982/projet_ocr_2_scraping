# coding: utf-8
import data_recovery as data


def main():
    # data.scraping_book_description()
    # data.scraping_book_by_categorie()
    urls_categories = data.scraping_category()
    data.scraping_book_by_categorie(urls_categories)


if __name__ == '__main__':
    main()
