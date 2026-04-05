from bot_instance import bot
from db.database import init_db
from handlers import start, create

start.register_handlers()
create.register_handlers()

init_db()
bot.infinity_polling(timeout=60, long_polling_timeout=60)