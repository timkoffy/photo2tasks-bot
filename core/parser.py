import json

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def parse_lesson_to_json(ocr_text: str, additional_requirements: str = "") -> dict:
    if not ocr_text or not ocr_text.strip():
        return None

    prompt = f"""
    Твоя задача — проанализировать распознанный текст с фотографии и преобразовать его в JSON.
    
    ДОПОЛНИТЕЛЬНЫЕ ТРЕБОВАНИЯ (ВЫСШИЙ ПРИОРИТЕТ, НАРУШАЮТ ОБЫЧНЫЕ ПРАВИЛА):
    {additional_requirements if additional_requirements else "Нет"}
    
    Если в требованиях сказано "не учитывай вопрос X" — ТЫ ОБЯЗАН УДАЛИТЬ ЭТОТ ПУНКТ ИЗ items. НЕ ВКЛЮЧАЙ ЕГО НИ ПРИ КАКИХ УСЛОВИЯХ.
    
    Схема JSON (МАССИВ секций):
    [
      {{
        "title": "Название секции 1",
        "items": ["Пункт 1", "Пункт 2", ...]
      }},
      {{
        "title": "Название секции 2",
        "items": ["Пункт 1", "Пункт 2", ...]
      }},
      и тд.
    ]
    
    ПРАВИЛА ГРУППИРОВКИ:
    1. Найди в тексте ЗАГОЛОВКИ разделов. Обычно они выглядят так:
       - "1. Изучение теоретических вопросов"
       - "2. Выполнение практических заданий"  
       - "3. Подготовка докладов"
       - "Теоретические вопросы", "Практические задания", "Темы докладов"
    
    2. Для КАЖДОГО такого заголовка создай ОТДЕЛЬНЫЙ объект в массиве:
       - "title" — текст заголовка (очищенный от нумерации)
       - "items" — все пункты, которые идут после этого заголовка и до следующего(в соотвествии с доп. требованиями)
    
    3. Если заголовок имеет нумерацию (например, "1. Изучение...") — УДАЛИ нумерацию, оставь только текст: "Изучение теоретических вопросов"
    
    4. Если в тексте нет явных заголовков, создай ОДИН объект с title "Основные вопросы"
    
    5. УДАЛИ ВСЮ НУМЕРАЦИЮ из пунктов внутри items (цифры, точки, символы типа $, !)
    
    6. НЕ ВКЛЮЧАЙ сами заголовки в items
    
    7. Верни ТОЛЬКО JSON-массив, без пояснений
    
    Текст для обработки:
    {ocr_text[:6000]}
    """

    print(prompt)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
    )

    # arcee-ai/trinity-large-preview:free

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3.6-plus:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6,
        )

        json_string = response.choices[0].message.content

        result = json.loads(json_string)
        print("ВЫХЛОП: ", result)
        return result

    except Exception:
        print("error trying text->json")
        return None