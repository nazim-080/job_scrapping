from random import randint

import requests
import time
from bs4 import BeautifulSoup as bs


def hh(url, city=None, language=None):
    jobs = []
    errors = []
    page = 0
    while True:
        try:
            resp = requests.get(f'{url}&period=1&page={page}').json()

            if 'items' in resp.keys():
                if len(resp['items']) > 0:
                    items = resp['items']
                    for item in items:
                        if item['snippet']['responsibility'] is None:
                            item['snippet']['responsibility'] = ''
                        if item['snippet']['requirement'] is None:
                            item['snippet']['requirement'] = ''
                        jobs.append({
                            'title': item['name'],
                            'url': item['alternate_url'],
                            'description': item['snippet']['responsibility'] + '\n' + item['snippet']['requirement'],
                            'company': item['employer']['name'],
                            'city_id': city,
                            'language_id': language,
                        })
                    page += 1
                else:
                    break
            else:
                errors.append({'url': url, 'error': resp['errors']})
                break
        except Exception:
            errors.append({'url': url, 'error': Exception})
    return jobs, errors


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def avito(url, city=None, language=None):
    domain = 'https://www.avito.ru'
    company = 'No name'
    jobs = []
    errors = []
    page = 1
    while True:
        time.sleep(3)
        try:
            resp = requests.get(url=f'{url}&p={page}', headers=headers)
            if resp.status_code == 200:
                soup = bs(resp.content, 'html.parser')
                if soup.find('div', attrs={'data-marker': 'catalog-serp'}).div:
                    main_div = soup.find('div', attrs={'data-marker': 'catalog-serp'})
                    div_list = main_div.find_all('div', attrs={'data-marker': 'item'})
                    for div_l in div_list:
                        title = div_l.find('a', attrs={'data-marker': 'item-title'}).h3.text
                        href = div_l.find('a', attrs={'data-marker': 'item-title'})['href']
                        description = div_l.find('div', attrs={'class': 'iva-item-descriptionStep-C0ty1'}).div.text
                        if div_l.find('a', attrs={'data-marker': 'item-link'}):
                            company = div_l.find('a', attrs={'data-marker': 'item-link'}).text
                        jobs.append({
                            'title': title,
                            'url': domain + href,
                            'description': description,
                            'company': company,
                            'city_id': city,
                            'language_id': language,
                        })
                else:
                    break
            else:
                errors.append({'url': url, 'error': f'Error code {resp.status_code}'})
                break
            page += 1
        except Exception:
            errors.append({'url': url, 'error': Exception})
    return jobs, errors

