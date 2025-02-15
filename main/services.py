# main/services.py

import openai
from django.conf import settings
from .models import ChatHistory

openai.api_key = settings.OPENAI_API_KEY

def translate_text_api(source_lang, target_lang, text):
    """Перевод текста через OpenAI API"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a translator. Translate from {source_lang} to {target_lang}."},
            {"role": "user", "content": text},
        ]
    )
    return response["choices"][0]["message"]["content"]

def generate_comment_api(target_lang, translation, comment_request):
    """Генерация комментария к переводу"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant providing explanations. Respond in {target_lang}."},
            {"role": "user", "content": f"Translation: {translation}. {comment_request}"},
        ]
    )
    return response["choices"][0]["message"]["content"]

def save_chat_to_db(user, input_text, translated_text, comment):
    """Сохранение чата в базу данных"""
    ChatHistory.objects.create(
        user=user,
        input_text=input_text,
        translated_text=translated_text,
        comment=comment
    )

def get_user_chat_history(user):
    """Получение истории чатов для пользователя"""
    return ChatHistory.objects.filter(user=user).order_by("-created_at")
