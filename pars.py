import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

company_list = ['innotech', 'selectel']
parsing = []



def parse(url):
    article = []
    date_list=[]
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    name = soup.find('a', class_='tm-company-card__name').get_text().strip()
    rate = soup.find('span', class_='tm-votes-lever__score-counter tm-votes-lever__score-counter tm-votes-lever__score-counter_rating').get_text().strip()
    industries = soup.find('div', class_='tm-company-profile__categories').get_text().strip()
    industries =' '.join(industries.split())
    about = soup.find('span', class_='tm-company-profile__content').get_text().strip().replace("\r"," ").replace("\n"," ").replace('\xa0', ' ')
    url_blog=soup.find_all('a', class_='tm-tabs__tab-link tm-tabs__tab-link')
    for ur in url_blog:
        main_url=ur.get('href')
        break
    article_urls_list=[]
    r_blog = requests.get(f'https://habr.com{main_url}')
    soup = bs(r_blog.text, "html.parser")
    article_urls = soup.find_all('a', class_='tm-title__link')
    

    for au in article_urls:
        art_url=au.get('href')
        article_urls_list.append(art_url)
    for item in article_urls_list:
        response = requests.get(f'https://habr.com{item}')
        soup=bs(response.text, "html.parser")
        refs = soup.find('div', xmlns='http://www.w3.org/1999/xhtml').text.strip().replace("\r"," ").replace("\n"," ").replace('\xa0', ' ')
        date = soup.find('span', class_='tm-article-datetime-published').text.strip()
        date =' '.join(date.split()) 
        article.append(refs)
        date_list.append(date)
    result = {
        'name': name,
        'rate': rate,
        'industries': industries,
        'about': about,
        'refs': article,
        'date_refs': date_list,
    }
    return result
for i in company_list:
    b = parse(f'https://habr.com/ru/companies/{i}/profile/')
    parsing.append(b)
df = pd.DataFrame(data=parsing)  
