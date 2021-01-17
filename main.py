import requests
from bs4 import BeautifulSoup
import csv

HOST = 'http://astana.gov.kz'
URL = 'http://astana.gov.kz/ru/search?query=covid'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}

news_list1 = []


# PAGINATION = input("Enter number of pages to be parsed, Введите количество страниц для парсинга")
# PAGINATION = int(PAGINATION.strip())

def get_html_page(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup1 = BeautifulSoup(html.content, 'html.parser')
    news_items1 = soup1.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['result'])
    return_list = []
    for news_item1 in news_items1:
        return_list.append(
            {
                'date': news_item1.find(class_='result-date').get_text(),
                'title': news_item1.find(class_='result-title').find('a').get_text().strip(),
                'link': HOST + news_item1.find(class_='result-title').find('a').get('href')
            }
        )
    return return_list


req = get_html_page(URL)

some_list = get_content(req)
print((len(some_list)))
# soup = BeautifulSoup(req.content, 'html.parser')

# Лямбда что бы ограничить результаты только классом 'result' который содержит заголовки.
# В противном случае результатов будет слишком много.
# news_items = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['result'])

# for news_item in news_items:
#     news_list.append(
#         {
#             'date': news_item.find(class_='result-date').get_text(),
#             'title': news_item.find(class_='result-title').find('a').get_text().strip(),
#             'link': HOST + news_item.find(class_='result-title').find('a').get('href')
#         }
#     )
# Информация попадает в лист со словарями.
keys = some_list[0].keys()
with open('parse_data.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(some_list)
