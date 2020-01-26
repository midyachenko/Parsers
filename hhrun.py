import requests, time,csv
from bs4 import  BeautifulSoup as bs

headers={'accept':'*/*',
         'user-agent': 'Chrome/79.0.3945.130'}
base_url='https://hh.ru/search/vacancy?order_by=publication_time&area=2&text=python&enable_snippets=true&search_period=7'

def hh_parse(base_url, headers):
    session = requests.Session()
    request=session.get(base_url, headers=headers)
    #time.sleep(3)

    if request.status_code==200:
        jobs=[]
        urls=[]
        urls.append(base_url)
        print('OK', request.status_code)
        soup= bs(request.content, 'html.parser')
        try:
            pagination=soup.find_all('a', attrs={'data-qa':'pager-page'})
            count=int(pagination[-1].text)
            print('Количество страниц: ', count)
            for i in range(count):
                url=f'https://hh.ru/search/vacancy?order_by=publication_time&area=2&text=python&enable_snippets=true&search_period=7&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'html.parser')

        #print(soup)
        divs=soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        print('Найдено вакансий:',len(divs))
        for div in divs:
            try:
                title=div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
                company=div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
                resp=div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                rec = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                '''print(title,'в ', company)
                print(resp)
                print(rec)
                print(href)'''
                jobs.append({'title': title,
                            'company': company,
                            'resp': resp,
                            'rec': rec,
                            'href': href})
            except:
                pass
        print(len(jobs))
        #for i in urls:
            #print(i)
        #for i in pagination:
            #print(i)

    else:
        print('Error!', request.status_code)
    session.close()
    return  jobs

def files_writer(jobs):
    with open('parsed_jobs.csv','w') as file:
        a_pen=csv.writer(file)
        a_pen.writerow(('Название вакансии', 'Название компании', 'Описание', 'Требования', 'URL' ))
        for job in jobs:
            a_pen.writerow((job['title'], job['company'],job['resp'], job['rec'], job['href']))


jobs=hh_parse(base_url, headers)
files_writer(jobs)