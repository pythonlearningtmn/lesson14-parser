import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup
from requests import get


def parser_html(req):
    data = []
    page = f'/feed/?q={req}'
    while page:
        note = []
        result = get(f'https://pythondigest.ru{page}')
        soup = BeautifulSoup(result.text, 'html.parser')
        for tag in soup.find_all('div', class_='item-container'):
            note = []
            title = tag.find(rel=['nofollow'])
            note_title = title.get_text()
            note_url = title.get('href')
            dat = tag.find('small')
            dat1 = re.search(r'\d{2}\.\d{2}\.\d{4}', dat.get_text())[0]
            dat2 = datetime.strptime(dat1, '%d.%m.%Y').date()
            note_date = dat2
            note.append(note_date)
            note.append(note_title)
            note.append(note_url)
            data.append(note)
        spisok = soup.find('ul', class_='pagination pagination-sm')
        if spisok:
            sp_end = spisok.find_all('li')[-1]
            page = sp_end.a.get('href')
        else:
            page = False

    columns = ['date', 'title', 'url']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv('news.csv')
    return data
