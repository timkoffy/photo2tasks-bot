from bot_instance import bot
from core.buttons import update_item_button
from db.database import create_session, add_item

def save_sections_to_db(chat_id: int, thread_id: int, sections: list, creator_username: str, creator_name: str):
    for section in sections:
        title = section.get("title", "Раздел")
        items = section.get("items", [])
        if not items:
            continue
        msg = bot.send_message(chat_id, f"📌 {title}\n\n🔄 Создаю кнопки...", message_thread_id=thread_id)
        session_uuid, session_id = create_session(
            chat_id=chat_id,
            thread_id=thread_id,
            message_id=msg.message_id,
            creator_username=creator_username,
            creator_name=creator_name,
            title=title
        )
        for idx, item_title in enumerate(items, 1):
            add_item(session_id, idx, item_title)
        update_item_button(chat_id, msg.message_id, session_id)