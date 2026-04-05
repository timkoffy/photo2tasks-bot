from bot import bot
from core.ocr_engine import photo2text_parser


def register_handlers():
    @bot.message_handler(commands=['create'])
    def create_command_without_photo(message):
        bot.send_message(message.chat.id, "❌ Пожалуйста, прикрепите фото с заданием к команде /create")

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        caption = message.caption or ""
        if caption.startswith('/create'):
            command_parts = caption.split(maxsplit=1)
            additional_requirements = command_parts[1] if len(command_parts) > 1 else ""

            chat_id = message.chat.id

            if additional_requirements:
                bot.send_message(chat_id, f"📝 Дополнительные требования добавлены в промпт: {additional_requirements}")

            bot.send_message(chat_id, "🔄 Начало конвертации...")

            text = photo2text_parser(message)
            if not text:
                bot.reply_to(message, "Не удалось распознать текст.")
            else:
                bot.reply_to(message, f"Распознано:\n{text}")
