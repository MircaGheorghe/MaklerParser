from datetime import datetime
from robot.models import *
from datetime import timedelta
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from django.db.models import Q
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading


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

TG_TOKEN = '968634038:AAEWvIuKILZwg45H0qtNoN7qZLSv90za37M'
bot = Bot(token=TG_TOKEN)
updater = Updater(bot=bot)

def start(bot, update):
    if User.objects.filter(last_name=update.message.chat_id).exists():
        update.message.reply_text('Sunteti conectat deja la acest bot')
        stop(bot, update)
    else:
        update.message.reply_text('Salut {}, pentru a primi informații despre anunțurile postate, scrie loginul tău de pe django admin.'.format(update.effective_chat.last_name))
        message_handler = MessageHandler(Filters.text, connect)
        updater.dispatcher.add_handler(message_handler)
        updater.start_polling()
        updater.idle()

def connect(bot, update):
    username = update.message.text
    last_name = update.message.chat_id
    if User.objects.filter(username=username).exists():
        new_user = User.objects.get(username = username)
        new_user.last_name = last_name
        new_user.save()
        bot.send_message(update.message.chat_id, text="Mulțumim, ai fost conectat cu succes")
        stop(bot, update)
    else:
        bot.send_message(update.message.chat_id, text="Utilizator cu astfe de login nu exista")

def send_message():
    pass


def get_chat_id():
    start_handler = CommandHandler("start", start)
    updater.dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

def shutdown():
    updater.stop()
    updater.is_idle = False

def stop(bot, update):
    threading.Thread(target=shutdown).start()
