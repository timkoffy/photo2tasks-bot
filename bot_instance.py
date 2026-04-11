import telebot
from dotenv import load_dotenv
import os
import requests

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")
ORIGINAL_URL = "https://api.telegram.org"

_old_request = requests.Session.request

def _patched_request(self, method, url, *args, **kwargs):
    if ORIGINAL_URL in url:
        url = url.replace(ORIGINAL_URL, PROXY_URL)
    return _old_request(self, method, url, *args, **kwargs)

requests.Session.request = _patched_request

bot = telebot.TeleBot(BOT_TOKEN)