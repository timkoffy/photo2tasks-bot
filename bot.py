from bot_instance import bot
from handlers import start, create

start.register_handlers()
create.register_handlers()

bot.infinity_polling()