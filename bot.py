import threading
import time

from bot_instance import bot
from db.database import init_db, delete_expired_sessions
from handlers import start, create, callback

def cleanup_scheduler():
    while True:
        delete_expired_sessions(days=30)
        time.sleep(3600)

init_db()

threading.Thread(target=cleanup_scheduler, daemon=True).start()

start.register_handlers()
create.register_handlers()
callback.register_handlers()

bot.infinity_polling()