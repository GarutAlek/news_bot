import requests
from fake_useragent import UserAgent
import json


url = 'https://tass.ru/tgap/api/v1/messages/?lang=ru&limit=15'

ua = UserAgent()
headers = {'User-Agent': str(ua.chrome)}


def get_tass_data_file():
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)
    with open('data/tass/tass.json', 'w', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)


def what_new_on_tass():
    res = {
        'tittles': [],
        'urls': []
    }
    with open('data/tass/tass.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    data = data['result']
    stage1 = {'tittles': [data[i]['body'].replace('<p>', '').replace('</p>', '') for i in range(len(data))],
              'urls': ['tass.ru' + data[i]['content_url'] for i in range(len(data))]}

    get_tass_data_file()
    with open('data/tass/tass.json', 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    data = data['result']
    stage2 = {'tittles': [data[i]['body'].replace('<p>', '').replace('</p>', '') for i in range(len(data))],
              'urls': ['tass.ru' + data[i]['content_url'] for i in range(len(data))]}

    for i in range(len(stage2['urls'])):
        if stage2['urls'][i] not in stage1['urls']:
            res['tittles'].append(f"<b>{stage2['tittles'][i]}</b>")
            res['urls'].append(stage2['urls'][i])
    with open('data/tass/tass_new.json', 'w', encoding='utf-8') as file:
        json.dump(res, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    what_new_on_tass()
