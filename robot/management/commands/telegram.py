from django.core.management.base import BaseCommand
from robot.models import *
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
        TG_TOKEN = '968634038:AAEWvIuKILZwg45H0qtNoN7qZLSv90za37M'
        bot = Bot(token=TG_TOKEN)
        updater = Updater(bot=bot)

        def start(bot, update):
            if User.objects.filter(last_name=update.message.chat_id).exists():
                update.message.reply_text('Sunteti conectat deja la acest bot')
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
            else:
                bot.send_message(update.message.chat_id, text="Utilizator cu astfe de login nu exista")

        def shutdown():
            updater.stop()
            updater.is_idle = False

        def stop(bot, update):
            threading.Thread(target=shutdown).start()

        start_handler = CommandHandler("start", start)
        updater.dispatcher.add_handler(start_handler)
        updater.start_polling()
        updater.idle()
