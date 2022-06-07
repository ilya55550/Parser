import requests
import xlsxwriter
from bs4 import BeautifulSoup
from time import sleep
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}




def generator_link_products():
    url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
    response = requests.get(url, headers=headers)
    bsoup = BeautifulSoup(response.text, 'lxml')
    paginator = bsoup.find_all('a', class_='page-link')
    last_page = [el_paginator.text for el_paginator in paginator][-2]

    for page in range(1, int(last_page) + 1):
        url = f'https://scrapingclub.com/exercise/list_basic/?page={page}'
        response = requests.get(url, headers=headers)
        bsoup = BeautifulSoup(response.text, 'lxml')
        product_cards = bsoup.find_all('div', class_='col-lg-4 col-md-6 mb-4')

        for product_card in product_cards:
            url_product = 'https://scrapingclub.com' + product_card.find('a').get('href')
            yield url_product


def parse_card_product():
    products = []
    for link_product in generator_link_products():
        response = requests.get(link_product, headers=headers)
        bsoup = BeautifulSoup(response.text, 'lxml')
        data_product = bsoup.find('div', class_='card mt-4 my-4')
        title = data_product.find('h3', class_='card-title').text
        price = data_product.find('h4').text
        description = data_product.find('p', class_='card-text').text
        image_url = 'https://scrapingclub.com/' + data_product.find('img', class_='card-img-top img-fluid').get('src')

        products.append((title, price, description, image_url))
    return products


def main():
    start_time = time.time()
    res = parse_card_product()

    for i in res:
        print(i)

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
