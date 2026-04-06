from bot_instance import bot
from core.buttons import send_items_as_buttons
from db.database import create_session, add_item

# todo: 30 days life period for session
def save_sections_to_db(message, sections: list, creator_username: str, creator_name: str):
    for section in sections:
        title = section.get("title", "Раздел")
        items = section.get("items", [])

        if not items:
            continue

        msg = bot.reply_to(message, f"📌 {title}\n\nСоздаю кнопки...")

        session_uuid, session_id = create_session(
            chat_id=message.chat.id,
            message_id=message.message_id,
            creator_username=creator_username,
            creator_name=creator_name,
            title=title
        )

        for idx, item_title in enumerate(items, 1):
            add_item(session_id, idx, item_title)

        send_items_as_buttons(message.chat.id, msg.message_id, session_id, title, items)
