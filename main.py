import requests
from bs4 import BeautifulSoup
import csv

HOST = 'http://astana.gov.kz'
URL = 'http://astana.gov.kz/ru/search?query=covid'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}


def get_html_page(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    # Лямбда что бы ограничить результаты только классом 'result' который содержит заголовки.
    news_items = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['result'])
    return_list = []
    for news_item in news_items:
        return_list.append(
            {
                'date': news_item.find(class_='result-date').get_text(),
                'title': news_item.find(class_='result-title').find('a').get_text().strip(),
                'link': HOST + news_item.find(class_='result-title').find('a').get('href')
            }
        )
    return return_list


def csv_writer(list_of_dictionaries):
    keys = list_of_dictionaries[0].keys()
    with open('parse_data.csv', 'w', newline='', encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dictionaries)


def parser_main_func():
    PAGINATION = input("Enter number of pages to be parsed, Введите количество страниц для парсинга")
    PAGINATION = int(PAGINATION.strip()) + 1
    req = get_html_page(URL)
    if req.status_code == 200:
        list_of_items = []
        for page in range(1, PAGINATION):
            print(f'Parsing page:{page}, идет парсинг страницы:{page}')
            html = get_html_page(URL, params={'page': page})
            list_of_items.extend(get_content(html))
        csv_writer(list_of_items)
        print('Finished. Готово.')
    else:
        print('Error')


parser_main_func()
