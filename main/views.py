# main/views 

from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
from .translations import TRANSLATIONS  # Импортируем переводы
import os
import json
from django.utils.translation import gettext_lazy as _


# def index(request):
#     return render(request, 'main/index.html'

# Вьюха для страницы "About"
def about(request):
    return render(request, 'main/about.html')

# Вьюха для страницы "Contact"
def contact(request):
    return render(request, 'main/contact.html')


def main_page(request):
    return render(request, 'main/main.html')

openai.api_key = os.getenv("OPENAI_API_KEY")



def get_translations(lang):
    """
    Получение переводов для выбранного языка.
    Если язык не найден, возвращается английская версия.
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"])



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

@login_required
def translate_text(request):
    """Основное представление для перевода с локализацией заголовков"""
    # Получаем выбранный язык из GET-запроса (или используем по умолчанию английский)
    selected_lang = request.GET.get("lang", "English")
    translations = get_translations(selected_lang)  # Получаем переводы для выбранного языка

    chat_history = ChatHistory.objects.filter(user=request.user).order_by("-created_at")  # Загружаем историю

    if request.method == "POST":
        source_lang = request.POST.get("source_lang")
        target_lang = request.POST.get("target_lang")
        text = request.POST.get("text")
        comment_request = request.POST.get("comment_request")

        # Перевод текста
        translation = translate_text_api(source_lang, target_lang, text)
        # Генерация комментария (если есть запрос)
        comment = generate_comment_api(target_lang, translation, comment_request) if comment_request else None

        # Сохранение в БД
        save_chat_to_db(request.user, text, translation, comment)

        return render(request, "main/translate.html", {
            "translation": translation,
            "comment": comment,
            "translations": translations,  # Передаем переводы в шаблон
            "selected_lang": selected_lang,  # Передаем текущий выбранный язык
            "chat_history": chat_history  # Передаем историю в шаблон
        })

    # Возвращаем форму с выбранным языком (если не POST)
    return render(request, "main/translate.html", {
        "translations": translations,  # Передаем переводы в шаблон
        "selected_lang": selected_lang,  # Передаем текущий выбранный язык
        "chat_history": chat_history  # Передаем историю
    })

