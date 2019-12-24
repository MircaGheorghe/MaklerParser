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
    phone_array = []
    soup = bs(requests.get(cat).content, 'html.parser')
    for article in soup.find('main', id = 'mainAnList').find('noscript').find('div', 'ls-detail').find_all('article'):
        phone = article.find('div', 'ls-detail_anData').find_all('span')[-1].text
        phone_array.append(phone)
        first = phone_array[0].replace('-', '')
    if not len(first.split(',')) > 1: #Daca este un singur numar, merge mai departe
        if Account.objects.filter(username__contains=first).exists(): #Daca numarul exista in baza de date,
            return False
        return True
    return False