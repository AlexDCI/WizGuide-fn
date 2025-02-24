# main/views 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import openai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ChatHistory
from .translations import TRANSLATIONS, languages # Импортируем переводы
import os
import json
from django.utils.translation import gettext_lazy as _
from .services import translate_text_api, generate_comment_api, save_chat_to_db, get_user_chat_history
from django.utils.translation import activate, get_language


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


# Функция для получения переводов интерфейса на выбранном языке
def get_interface_translations(selected_lang):
    """
    Получает переводы для выбранного языка интерфейса.
    Если перевод для языка не найден, возвращается английская версия.
    
    :param selected_lang: Язык интерфейса, выбранный пользователем
    :return: Словарь с переводами для выбранного языка
    """
    return get_translations(selected_lang)


# Функция для загрузки истории чатов пользователя
def load_chat_history(user):
    """
    Загружает историю чатов для пользователя из базы данных.
    
    :param user: Пользователь, для которого нужно загрузить историю
    :return: Список объектов истории чатов
    """
    return get_user_chat_history(user)


# Функция для обработки перевода и генерации комментариев
def handle_translation(source_lang, target_lang, text, comment_request):
    """
    Обрабатывает перевод текста с одного языка на другой и генерирует комментарий, если требуется.
    
    :param source_lang: Исходный язык
    :param target_lang: Целевой язык
    :param text: Текст для перевода
    :param comment_request: Запрос на создание комментария (если есть)
    :return: Переведенный текст и комментарий (если он был сгенерирован)
    """
    # Перевод текста
    translation = translate_text_api(source_lang, target_lang, text)
    
    # Генерация комментария (если есть запрос)
    comment = generate_comment_api(target_lang, translation, comment_request) if comment_request else None

    return translation, comment


# Функция для сохранения перевода в базу данных
def save_translation_to_db(user, input_text, translated_text, comment):
    """
    Сохраняет перевод текста и (опционально) комментарий в базу данных.
    
    :param user: Пользователь, чье сообщение сохраняется
    :param input_text: Исходный текст
    :param translated_text: Переведенный текст
    :param comment: Сгенерированный комментарий (если есть)
    """
    save_chat_to_db(user, input_text, translated_text, comment)


# Функция для редиректа на ту же страницу с сохранением выбранных языков
def redirect_to_same_page(source_lang, target_lang, selected_lang):
    """
    Осуществляет редирект на ту же страницу с сохранением исходного и целевого языка, а также языка интерфейса.
    
    :param source_lang: Исходный язык
    :param target_lang: Целевой язык
    :param selected_lang: Язык интерфейса
    :return: Перенаправление на ту же страницу с актуальными параметрами
    """
    return redirect(f'/translate?source_lang={source_lang}&target_lang={target_lang}&lang={selected_lang}')



# Основная функция для обработки запроса на перевод
@login_required
def translate_text(request):
    """
    Основная функция для обработки запроса на перевод текста.
    Обрабатывает сохранение языков в сессии и редирект с актуальными языковыми параметрами.
    """
    # Получаем выбранный язык интерфейса из GET-параметров или из сессии
    selected_lang = request.GET.get("lang", request.session.get("selected_lang", "English"))
    
    # Сохраняем язык интерфейса в сессии
    request.session["selected_lang"] = selected_lang
    
    # Получаем переводы для выбранного языка интерфейса
    translations = get_interface_translations(selected_lang)
    
    # Загружаем историю чатов
    chat_history = load_chat_history(request.user)
    
    # Получаем исходный и целевой языки из GET-запроса или из сессии
    source_lang = request.GET.get("source_lang", request.session.get("source_lang", "English"))
    target_lang = request.GET.get("target_lang", request.session.get("target_lang", "Russian"))
    
    # Сохраняем исходный и целевой языки в сессии
    request.session["source_lang"] = source_lang
    request.session["target_lang"] = target_lang

    if request.method == "POST":
        # Если метод POST, сохраняем новые языки из формы
        source_lang = request.POST.get("source_lang", source_lang)
        target_lang = request.POST.get("target_lang", target_lang)
        text = request.POST.get("text")
        comment_request = request.POST.get("comment_request")

        # Обрабатываем перевод и генерируем комментарий
        translation, comment = handle_translation(source_lang, target_lang, text, comment_request)
        
        # Сохраняем данные в базе
        save_translation_to_db(request.user, text, translation, comment)
        
        # Перенаправляем на страницу с актуальными параметрами
        return redirect_to_same_page(source_lang, target_lang, selected_lang)

    # Возвращаем форму с выбранным языком (если не POST)
    return render(request, "main/translate.html", {
        "translations": translations,  # Передаем переводы в шаблон
        "selected_lang": selected_lang,  # Передаем текущий выбранный язык
        "source_lang": source_lang,  # Берем язык из GET-запроса или по умолчанию
        "target_lang": target_lang,  # Берем язык из GET-запроса или по умолчанию
        "chat_history": chat_history,  # Передаем историю
        "languages": languages  # Передаем список языков
    })


