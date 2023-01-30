import re
import json
import pprint

from bs4 import BeautifulSoup
from requests import get


def new_parser1(req):
    new = f'/feed/?q={req}'
    results = {}
    result = []
    while new:
        res = get(f'https://pythondigest.ru{new}')
        soup = BeautifulSoup(res.text, 'html.parser')
        for tag in soup.find_all('div', class_='item-container'):
            title = tag.find(rel=['nofollow'])
            dat = tag.find('small')
            d1 = re.search(r'\d{2}\.\d{2}\.\d{4}', dat.get_text())[0]
            result.append({'date': d1,
                           'title': title.get_text(),
                           'link': title.get('href')})
        ss = soup.find('ul', class_='pagination pagination-sm')
        if ss:
            p = ss.find_all('li')[-1]
            new = p.a.get('href')
        else:
            new = False
    results['res'] = result
    with open('results.json', mode='w') as f:
        json.dump(results, f)
    return results
