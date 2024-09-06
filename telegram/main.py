#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 2 06:18:55 2024

@author: cabreu
"""

from flask import Flask, request, url_for, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import nest_asyncio
import requests
from threading import Thread


TELEGRAM_TOKEN = ''

FLASK_PORT = 4040
FLASK_SERVER_LINK =f'http://localhost:{FLASK_PORT}'

nest_asyncio.apply()

# esta funcion sirve para mandar mensajes directamente a un chat desde el bot
def send_telegram_message(message,chatId):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chatId,
        'text': message,
    }
    requests.post(url, data=payload)
    


# creando la instancia de flask
app_flask = Flask(__name__)

# creando la instancia del bot de telegram
app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# aqui podemos poner los comandos de telegram para llamar funciones y botones dentro 
"""

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_client)],
        BUSINESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_business)],
        PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone)],
    },
    fallbacks=[]
)

            
app_telegram.add_handler(conv_handler)
app_telegram.add_handler(CommandHandler('code', handle_code))
app_telegram.add_handler(CallbackQueryHandler(button))

"""

# creamos un hilo aparte para manejar flask y telegram separados
class FlaskThread(Thread):
    def run(self) -> None:
        app_flask.run(port=FLASK_PORT)

class TelegramThread(Thread):
    def run(self) -> None:
        app_telegram.run_polling()
        

if __name__ == '__main__':
    flask_thread=FlaskThread()
    flask_thread.daemon=True
    flask_thread.start()

    
    telegram_thread=TelegramThread()
    telegram_thread.daemon=True
    telegram_thread.start()



