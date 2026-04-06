from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_instance import bot
from db.database import get_items_by_session, get_selections_for_item, get_session_by_id

def send_items_as_buttons(chat_id: int, message_id: int, session_id: int, session_title: str, items: list):
    if not items:
        return

    db_items = get_items_by_session(session_id)
    if not db_items:
        text = f"📋 <b>{session_title}</b>:\n\n"
        for idx, title in enumerate(items, 1):
            text += f"{idx}. {title}\n   <i>Свободен</i>\n\n"
        markup = InlineKeyboardMarkup(row_width=1)
        for idx, title in enumerate(items, 1):
            button_text = f"{idx}. {title[:47]}..." if len(title) > 50 else f"{idx}. {title}"
            callback_data = f"select_{session_id}_{idx}"
            markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))
    else:
        text = f"📋 <b>{session_title}</b>:\n\n"
        for item in db_items:
            num = item['item_number']
            title = item['title']
            selections = get_selections_for_item(item['id'])
            if selections:
                names = []
                for sel in selections:
                    name = sel.get('username') or sel.get('first_name') or 'Аноним'
                    names.append(f"@{name}" if sel.get('username') else name)
                text += f"{num}. {title}\n   <i>Занят:</i> {', '.join(names)}\n\n"
            else:
                text += f"{num}. {title}\n   <i>Свободен</i>\n\n"
        markup = InlineKeyboardMarkup(row_width=1)
        for item in db_items:
            num = item['item_number']
            title = item['title']
            button_text = f"{num}. {title[:47]}..." if len(title) > 50 else f"{num}. {title}"
            callback_data = f"select_{session_id}_{num}"
            markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )

def update_item_button(chat_id: int, message_id: int, session_id: int):
    session = get_session_by_id(session_id)
    if not session:
        return
    session_title = session['title']

    items = get_items_by_session(session_id)

    text = f"📋 <b>{session_title}</b>:\n\n"
    for item in items:
        num = item['item_number']
        title = item['title']
        selections = get_selections_for_item(item['id'])
        if selections:
            names = []
            for sel in selections:
                name = sel.get('username') or sel.get('first_name') or 'Аноним'
                names.append(f"@{name}" if sel.get('username') else name)
            text += f"{num}. {title}\n   <i>Занят:</i> {', '.join(names)}\n\n"
        else:
            text += f"{num}. {title}\n   <i>Свободен</i>\n\n"

    markup = InlineKeyboardMarkup(row_width=1)
    for item in items:
        num = item['item_number']
        title = item['title']
        button_text = f"{num}. {title[:47]}..." if len(title) > 50 else f"{num}. {title}"
        callback_data = f"select_{session_id}_{num}"
        markup.add(InlineKeyboardButton(button_text, callback_data=callback_data))

    markup.add(InlineKeyboardButton("❌ Очистить выборы", callback_data=f"clear_my_{session_id}"))

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=markup,
        parse_mode="HTML"
    )