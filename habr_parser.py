import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json


url = 'https://habr.com/ru/news/page1/'

ua = UserAgent()
headers = {'User-Agent':str(ua.chrome)}


def get_habr_data_file():
    response = requests.get(url, headers=headers)
    with open('data/habr/index.html', 'w', encoding='utf-8') as file:
        file.write(response.text)


def get_habr_data():
    with open('data/habr/index.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'lxml')
    article_urls = []
    article_tittles = []
    article_text = []
    for tittles in soup.find_all('a', class_="tm-article-snippet__title-link"):
        for tittle in tittles.find_all('span', class_=""):
            article_tittles.append(tittle.text)

    for a_url in soup.find_all('a', class_='tm-article-snippet__title-link'):
        article_urls.append('habr.com' + a_url['href'])

    for text in soup.find_all('div', class_=("article-formatted-body article-formatted-body article-formatted-body_version-1", "article-formatted-body article-formatted-body article-formatted-body_version-2")):
        article_text.append(text.text.replace('\n', ''))

    res = {'tittles': article_tittles,
            'urls': article_urls,
            'texts': article_text }

    with open('data/habr/habr.json', 'w', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)


def what_new_on_habr():
    with open('data/habr/habr.json', 'r', encoding='utf-8') as file:
        stage1 = json.loads(file.read())
    get_habr_data_file()
    get_habr_data()
    with open('data/habr/habr.json', 'r', encoding='utf-8') as file:
        stage2 = json.loads(file.read())

    with open('data/habr/habr_new.json', 'w', encoding='utf-8') as file:
        res = {'tittles': [],
               'texts': [],
               'urls': []
               }
        for i in range(len(stage2['urls'])):
            if stage2['urls'][i] not in stage1['urls']:
                res['tittles'].append(f"<b>{stage2['tittles'][i]}</b>")
                res['texts'].append(stage2['texts'][i])
                res['urls'].append(stage2['urls'][i])
        json.dump(res, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    what_new_on_habr()