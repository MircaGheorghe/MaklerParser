from datetime import datetime
from robot.models import *
from datetime import timedelta
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from django.db.models import Q


def get_valid_links(cat):
    # Aici fa asa ca sa se posteze cele care sunt noi, adica fara data si ora
    date_24h = datetime.now() - timedelta(hours=24)
    links = Link.objects.filter(Q(post_date__lt = date_24h) | Q(post_date = None), category=cat)
    if links:
        return links
    if Link.objects.filter(category=cat, payment=True, posted=False).exists():
        return Link.objects.filter(category=cat, payment = True, posted=False)
    else:
        Link.objects.update(posted=False)
    return links



def get_last_phone(cat):
    phone_array = []
    soup = bs(requests.get(cat).content, 'html.parser')
    for article in soup.find('main', id = 'mainAnList').find('noscript').find('div', 'ls-detail').find_all('article'):
        try:
            phone = article.find('div', 'ls-detail_anData').find_all('span')[-1].text
        except:
            pass
        phone_array.append(phone)
        first = phone_array[0].replace('-', '')
    print(first)
    if not len(first.split(',')) > 1:
        if Account.objects.filter(username__contains=first).exists(): #Daca numarul exista in baza de date,
            return True
        return False
    else:
        return False
    return True
