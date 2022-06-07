import requests
import xlsxwriter
from bs4 import BeautifulSoup
from time import sleep

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}


def download_image(url_image):
    """Скачивание изображения товара"""
    response = requests.get(url_image, stream=True)
    with open('/home/ilya/Рабочий стол/image/' + url_image.split('/')[-1], 'wb') as file:
        for value in response.iter_content(1024 * 1024):
            file.write(value)


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


def generator_card_product():
    count = 0
    for link_product in generator_link_products():
        # sleep(0.5)
        response = requests.get(link_product, headers=headers)
        bsoup = BeautifulSoup(response.text, 'lxml')
        data_product = bsoup.find('div', class_='card mt-4 my-4')
        title = data_product.find('h3', class_='card-title').text
        price = data_product.find('h4').text
        description = data_product.find('p', class_='card-text').text
        image_url = 'https://scrapingclub.com/' + data_product.find('img', class_='card-img-top img-fluid').get('src')
        download_image(image_url)
        print(count)
        count += 1
        yield title, price, description, image_url


def writer(func):
    """Запись в файл формата xlsx"""
    with xlsxwriter.Workbook('/home/ilya/Рабочий стол/data.xlsx') as file:
        page = file.add_worksheet('товар')

        row = 0
        column = 0

        page.set_column('A:A', 20)
        page.set_column('B:B', 20)
        page.set_column('C:C', 50)
        page.set_column('D:D', 50)

        for card_product in func():
            page.write(row, column, card_product[0])
            page.write(row, column + 1, card_product[1])
            page.write(row, column + 2, card_product[2])
            page.write(row, column + 3, card_product[3])
            row += 1


def main():
    writer(generator_card_product)


if __name__ == '__main__':
    main()
