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
from .services import translate_text_api, generate_comment_api, save_chat_to_db, get_user_chat_history


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

def get_translations(lang):
    """
    Получение переводов для выбранного языка.
    Если язык не найден, возвращается английская версия.
    """
    return TRANSLATIONS.get(lang, TRANSLATIONS["English"])

# @login_required
# def translate_text(request):
#     """Основное представление для перевода с локализацией заголовков"""
#     # Получаем выбранный язык из GET-запроса (или используем по умолчанию английский)
#     selected_lang = request.GET.get("lang", "English")
#     translations = get_translations(selected_lang)  # Получаем переводы для выбранного языка

#     # Загружаем историю чатов
#     chat_history = get_user_chat_history(request.user)

#     if request.method == "POST":
#         source_lang = request.POST.get("source_lang")
#         target_lang = request.POST.get("target_lang")
#         text = request.POST.get("text")
#         comment_request = request.POST.get("comment_request")

#         # Перевод текста
#         translation = translate_text_api(source_lang, target_lang, text)
#         # Генерация комментария (если есть запрос)
#         comment = generate_comment_api(target_lang, translation, comment_request) if comment_request else None

#         # Сохранение в БД
#         save_chat_to_db(request.user, text, translation, comment)

#         return render(request, "main/translate.html", {
#             "translation": translation,
#             "comment": comment,
#             "translations": translations,  # Передаем переводы в шаблон
#             "selected_lang": selected_lang,  # Передаем текущий выбранный язык
#             "chat_history": chat_history  # Передаем историю в шаблон
#         })

#     # Возвращаем форму с выбранным языком (если не POST)
#     return render(request, "main/translate.html", {
#         "translations": translations,  # Передаем переводы в шаблон
#         "selected_lang": selected_lang,  # Передаем текущий выбранный язык
#         "chat_history": chat_history  # Передаем историю
#     })


@login_required
def translate_text(request):
    """Основное представление для перевода с локализацией заголовков"""
    
    # Список доступных языков
    languages = [
        "English", "Russian", "German", "Spanish", "French", "Italian", 
        "Portuguese", "Chinese", "Chinese-Traditional", "Japanese", "Korean", 
        "Arabic", "Hindi", "Bengali", "Urdu", "Turkish", "Dutch", "Greek", 
        "Polish", "Czech", "Hungarian", "Swedish", "Danish", "Finnish", "Norwegian", 
        "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay", "Filipino", 
        "Romanian", "Slovak", "Bulgarian", "Croatian", "Serbian", "Slovenian", 
        "Lithuanian", "Latvian", "Estonian", "Georgian", "Armenian", "Persian", 
        "Pashto", "Azerbaijani", "Kazakh", "Uzbek", "Tajik", "Turkmen", "Kyrgyz", 
        "Mongolian", "Swahili", "Zulu", "Xhosa", "Afrikaans", "Haitian Creole", 
        "Basque", "Galician", "Catalan", "Irish", "Welsh", "Scottish Gaelic", 
        "Maltese", "Icelandic", "Sanskrit", "Tibetan", "Maori", "Samoan", "Tongan"
    ]

    # Получаем выбранный язык из GET-запроса (или используем по умолчанию английский)
    selected_lang = request.GET.get("lang", "English")
    translations = get_translations(selected_lang)  # Получаем переводы для выбранного языка

    # Загружаем историю чатов
    chat_history = get_user_chat_history(request.user)

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
            "chat_history": chat_history,  # Передаем историю в шаблон
            "languages": languages  # Передаем список языков
        })

    # Возвращаем форму с выбранным языком (если не POST)
    return render(request, "main/translate.html", {
        "translations": translations,  # Передаем переводы в шаблон
        "selected_lang": selected_lang,  # Передаем текущий выбранный язык
        "chat_history": chat_history,  # Передаем историю
        "languages": languages  # Передаем список языков
    })