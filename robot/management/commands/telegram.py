#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from robot.models import *

import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from django.contrib.auth.models import User

# Enable logging
TG_TOKEN = '968634038:AAEWvIuKILZwg45H0qtNoN7qZLSv90za37M'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [['Introducerea Usernameului']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(update, context):
    update.message.reply_text('Salut {}, pentru a primi informații despre anunțurile postate, scrie loginul tău de pe django admin.'.format(update.effective_chat.last_name))

    return TYPING_REPLY


def regular_choice(update, context):
    text = update.message.text
    context.user_data['choice'] = text
    update.message.reply_text('Introduceți usernameul:')

    return TYPING_REPLY

def received_information(update, context):
    user_data = context.user_data
    text = update.message.text
    chat_id = update.message.chat_id
    if User.objects.filter(username = text).exists():
        User.objects.filter(username = text).update(last_name = chat_id)
        update.message.reply_text("Veți primi notificările de pe contul {} în acest chat.".format(text))
        done(update, context)
    else:
        User.objects.filter(username = text).update(last_name = chat_id)
        update.message.reply_text("Nu există așa cont, {}. Vă rugăm introduceți alt cont".format(text))
        return TYPING_REPLY

def done(update, context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("Vă mulțumim\n Puteți introduce un alt username pentru a fi adăugat în baza de date.")
    user_data.clear()
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    def handle(self, *args, **options):
        updater = Updater(TG_TOKEN, use_context=True)

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={
                CHOOSING: [MessageHandler(Filters.regex('^(Introducerea Usernameului)$'),
                                            regular_choice),
                            ],

                TYPING_CHOICE: [MessageHandler(Filters.text,
                                                regular_choice)
                                ],

                TYPING_REPLY: [MessageHandler(Filters.text,
                                                received_information),
                                ],
            },

            fallbacks=[MessageHandler(Filters.regex('^Nimic$'), done)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()