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

# TG_TOKEN = '968634038:AAEWvIuKILZwg45H0qtNoN7qZLSv90za37M'
# bot = Bot(token=TG_TOKEN)
# updater = Updater(bot=bot)

# def start(bot, update):
#     print("sdfasdf")
#     update.message.reply_text('Salut {}, acum vei primi informatia despre noile postări aici.'.format(update.effective_chat.last_name))
#     # stop(bot, update)

# def do_makler(bot, update):
#     print("ddssa")
#     text = update.message.text
#     print(text)

# # def send_message(link, user, date):
# #     text = "Link-ul postat: {}\r\n User: {}\r\n Data: {}".format(link, user, date)
# #     user = request.user
# #     accounts = user.account_user.all
# #     print(user.id)
# #     # user = User.objects.get(first = username)
# #     # user.username = newusername
# #     # user.save()
# #     bot.send_message(id, text=text)

# # def send_error_message(text):
# #     f = open("chat_id.txt", "r")
# #     id = f.read()
# #     bot.send_message(id, text=text)
# #     f.close()
# print("dasd")
# start_handler = CommandHandler("start", start)
# message_handler = MessageHandler(Filters.text, do_makler)

# updater.dispatcher.add_handler(message_handler)
# updater.dispatcher.add_handler(start_handler)


# # def shutdown():
# #     updater.stop()
# #     updater.is_idle = False

# # def stop(bot, update):
# #     threading.Thread(target=shutdown).start()
TG_TOKEN = '968634038:AAEWvIuKILZwg45H0qtNoN7qZLSv90za37M'
bot = Bot(token=TG_TOKEN)
updater = Updater(bot=bot)

def start(bot, update):
    update.message.reply_text('Hello {}!'.format(update.effective_chat.first_name))

def do_makler(bot, update):
    text = update.message.text
    print(text)


start_handler = CommandHandler("start", start)
message_handler = MessageHandler(Filters.text, do_makler)

updater.dispatcher.add_handler(message_handler)
updater.dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()