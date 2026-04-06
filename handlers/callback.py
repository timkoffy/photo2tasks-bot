from bot_instance import bot
from db.database import select_item, get_items_by_session, clear_user_selections
from core.buttons import update_item_button

def register_handlers():
    @bot.callback_query_handler(func=lambda call: call.data.startswith("select_"))
    def handle_select(call):
        _, session_id_str, item_number_str = call.data.split("_")
        session_id = int(session_id_str)
        item_number = int(item_number_str)

        user = call.from_user

        items = get_items_by_session(session_id)
        target_item = None
        for item in items:
            if item['item_number'] == item_number:
                target_item = item
                break

        if not target_item:
            bot.answer_callback_query(call.id, "Пункт не найден", show_alert=True)
            return

        success = select_item(
            item_id=target_item['id'],
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

        if success:
            update_item_button(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                session_id=session_id,
            )
            bot.answer_callback_query(call.id, f"✅ Вы записаны на пункт {item_number}")
        else:
            bot.answer_callback_query(call.id, "❌ Вы уже записаны на этот пункт", show_alert=True)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("clear_my_"))
    def handle_clear_my_selections(call):
        session_id = int(call.data.split("_")[2])
        user_id = call.from_user.id
        deleted = clear_user_selections(session_id, user_id)
        if deleted:
            update_item_button(call.message.chat.id, call.message.message_id, session_id)
            bot.answer_callback_query(call.id, f"✅ Отменено {deleted} выборов")
        else:
            bot.answer_callback_query(call.id, "❌ У вас не было выборов в этой сессии", show_alert=True)