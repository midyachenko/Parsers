import requests, time
from bs4 import  BeautifulSoup as bs

headers={'accept':'*/*',
         'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'}
base_url='https://hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=python&enable_snippets=true&search_period=7&page=0'

def hh_parse(base_url, headers):
    session = requests.Session()
    request=session.get(base_url, headers=headers)
    time.sleep(3)

    if request.status_code==200:
        print('OK', request.status_code)
        soup= bs(request.content, 'html.parser')
        #print(soup)
        divs=soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        print('Найдено вакансий:',len(divs))
        for div in divs:
            title=div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
            company=div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
            resp=div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            rec = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            print(title,'в ', company)
            print(resp)
            print(rec)
            print(href)
    else:
        print('Error!', request.status_code)

    session.close()

hh_parse(base_url, headers)