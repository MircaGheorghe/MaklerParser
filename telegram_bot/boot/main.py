from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler

from config import TG_TOKEN

mybots = {}

bot = Bot(token=TG_TOKEN)
updater = Updater(bot=bot)

def start(bot, update):
    mybots[update.message.chat_id] = bot
    update.message.reply_text('Hello {}!'.format(update.effective_chat.first_name))

def send_later():
    print("dsa")
    for id, bot in mybots.items():
        bot.send_message(id, text='Beep!')

start_handler = CommandHandler("start", start)
updater.dispatcher.add_handler(start_handler)

updater.start_polling()
updater.idle()