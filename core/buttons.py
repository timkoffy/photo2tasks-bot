from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_instance import bot

# todo: button handlers
def send_items_as_buttons(chat_id: int, message_id: int, session_id: int, session_title: str, items: list):
    if not items:
        return

    text = f"📋 *{session_title}:*\n\n"
    for idx, item in enumerate(items, 1):
        text += f"{idx}. {item}\n"


    markup = InlineKeyboardMarkup(row_width=1)
    for idx, item in enumerate(items):
        button_text = f"{idx + 1}. {item[:47]}..." if len(item) > 50 else f"{idx + 1}. {item}"
        callback_data = f"select_{session_id}_{idx + 1}"
        markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))

    # markup.add(InlineKeyboardButton("Сбросить всё", callback_data=f"finish_{session_id}"))

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=markup,
        parse_mode="Markdown"
    )


def update_item_button(chat_id: int, message_id: int, session_id: int, item_number: int, username: str):
    pass