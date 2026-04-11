import pytesseract
from PIL import Image
import os
from bot_instance import bot

def photo2text_parser(message) -> str:
    chat_id = message.chat.id
    user_id = message.from_user.id
    temp_file_path = f"temp_photo_{user_id}_{chat_id}.jpg"
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(temp_file_path, 'wb') as f:
            f.write(downloaded_file)

        img = Image.open(temp_file_path)

        extracted_text = pytesseract.image_to_string(img, lang='rus')

        os.remove(temp_file_path)

        print("успешное преобразование изображение -> текст")

        return extracted_text.strip()

    except Exception:
        print("ОШИБКА преобразование изображение -> текст")
        return ""