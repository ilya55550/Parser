import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}


def generator_link_products():
    page = 1
    while True:
        url = f'https://www.lamoda.ru/c/517/clothes-muzhskie-bryuki/?page={page}'
        print(f'page: {page}')
        response = requests.get(url, headers=headers)

        bsoup = BeautifulSoup(response.text, 'lxml')
        product_cards = bsoup.find_all('div', class_='x-product-card__card')
        page += 1

        if product_cards:
            for product_card in product_cards:
                url_product = 'https://www.lamoda.ru/' + product_card.find('a').get('href')
                yield url_product
        else:
            print('Такой страницы с товаром нет')
            break


def parse_card_product():
    for link_product in generator_link_products():
        response = requests.get(link_product, headers=headers)
        bsoup = BeautifulSoup(response.text, 'lxml')
        try:
            data_product = bsoup.find('div', class_='product-title-wrapper')
            title = data_product.find('h1').get('title')
            name = data_product.find('span', class_='product-title__model-name').text
            price = bsoup.find('span', class_='product-prices__price').text
        except TypeError:
            print('Данные товара отсутвуют')
        print(f'{title}, {name}, {price}')


def main():
    parse_card_product()


if __name__ == '__main__':
    main()
