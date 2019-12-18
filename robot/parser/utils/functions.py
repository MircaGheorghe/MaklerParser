from datetime import datetime
from robot.models import *
from datetime import timedelta
import requests
import urllib.request
from bs4 import BeautifulSoup as bs


def get_valid_links(cat):
    date_24h = datetime.now() - timedelta(hours=24)
    links = Link.objects.filter(category=cat, post_date__lt = date_24h)
    if links:
        return links
    return Link.objects.filter(category=cat, payment = True)

def get_last_phone(cat):
    soup = bs(requests.get(cat).content, 'html.parser')
    for article in soup.find('main', id = 'mainAnList').find('noscript').find('div', 'ls-detail').find_all('article'):
        print(article.find('div', 'ls-detail_anData').find_all('span')[-1])
    return False
    # secv = soup.find('main', attrs={'id':'mainAnList'})
    # for sec in secv.find_all('div', class_ = 'ls-detail_anData'):
    #     print(sec.find('span'))