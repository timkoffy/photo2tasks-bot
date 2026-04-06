import json

from bot_instance import bot
from core.ocr_engine import photo2text_parser
from core.parser import parse_lesson_to_json
from db.manager import save_sections_to_db


def register_handlers():
    @bot.message_handler(commands=['create'])
    def create_command_without_photo(message):
        bot.send_message(message.chat.id, "❌ Пожалуйста, прикрепите фото с заданием к команде /create", message_thread_id=message.message_thread_id)

    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        caption = message.caption or ""
        if caption.startswith('/create'):
            command_parts = caption.split(maxsplit=1)
            additional_requirements = command_parts[1] if len(command_parts) > 1 else ""

            chat_id = message.chat.id
            thread_id = message.message_thread_id

            if additional_requirements:
                bot.send_message(chat_id, f"📝 Дополнительные требования добавлены в промпт: {additional_requirements}", message_thread_id=thread_id)

            bot.send_message(chat_id, "🔄 Начало конвертации...", message_thread_id=thread_id)

            text = photo2text_parser(message)

            if not text:
                bot.reply_to(message, "Не удалось распознать текст.", message_thread_id=thread_id)
            else:
                processed_json = parse_lesson_to_json(text, additional_requirements)
                # processed_json = [
                #     {
                #         "title": "Подготовка докладов",
                #         "items": [
                #             "Корниловский мятеж",
                #             "Продовольственная диктатура: причины введения и реализация",
                #             "Создание Красной Армии и ВЧК",
                #             "Итоги Учредительного собрания",
                #             "Деятельность Всероссийского съезда Советов",
                #             "Установление советской власти в центре страны и регионах на материалах Саратовской губернии",
                #             "Формирование однопартийной системы",
                #             "Установление советской власти в Саратове"
                #         ]
                #     }
                # ]
                if processed_json:
                    save_sections_to_db(
                        chat_id=message.chat.id,
                        thread_id=message.message_thread_id,
                        sections=processed_json,
                        creator_username=message.from_user.username,
                        creator_name=message.from_user.full_name
                    )