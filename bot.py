import telebot
from dotenv import load_dotenv
import os


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

from handlers import start, create

start.register_handlers()
create.register_handlers()

bot.infinity_polling()