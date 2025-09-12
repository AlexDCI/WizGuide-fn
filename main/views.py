# main/views 

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
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
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseServerError
from datetime import datetime, timedelta
import json, jwt
import requests
from django.conf import settings


@login_required
def issue_token(request):
    """Короткий JWT для FastAPI (действителен 30 минут)."""
    payload = {
        "user_id": request.user.id,
        "username": request.user.username,
        "exp": datetime.utcnow() + timedelta(minutes=30),
        "iss": "django"
    }
    token = jwt.encode(payload, settings.VOICE_JWT_SECRET, algorithm="HS256")
    return JsonResponse({"access": token})

@login_required
def save_speech_result(request):
    """Сохраняем распознанный текст и перевод в ChatHistory."""
    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    try:
        data = json.loads(request.body.decode("utf-8"))
        src = data.get("source_text") or ""
        trg = data.get("translated_text") or ""
        comment = data.get("comment")
        ChatHistory.objects.create(
            user=request.user,
            input_text=src,
            translated_text=trg,
            comment=comment
        )
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)


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

    # Получаем язык интерфейса
    selected_lang = request.GET.get("lang", request.session.get("selected_lang", "English"))
    request.session["selected_lang"] = selected_lang
    translations = get_interface_translations(selected_lang)

    # История чатов
    chat_history = load_chat_history(request.user)

    # Языки
    source_lang = request.GET.get("source_lang", request.session.get("source_lang", "English"))
    target_lang = request.GET.get("target_lang", request.session.get("target_lang", "Russian"))
    request.session["source_lang"] = source_lang
    request.session["target_lang"] = target_lang

    # Ошибка (если будет)
    error = None

    if request.method == "POST":
        source_lang = request.POST.get("source_lang", source_lang)
        target_lang = request.POST.get("target_lang", target_lang)
        text = request.POST.get("text", "")
        comment_request = request.POST.get("comment_request", "")

        # Проверка ограничений
        if len(text) > 1000:
            error = _("The text must not exceed 1000 characters.")
        elif comment_request and len(comment_request) > 1000:
            error = _("The comment must not exceed 1000 characters.")
        else:
            translation, comment = handle_translation(source_lang, target_lang, text, comment_request)
            save_translation_to_db(request.user, text, translation, comment)
            return redirect_to_same_page(source_lang, target_lang, selected_lang)

    # Рендерим шаблон
    return render(request, "main/translate.html", {
        "translations": translations,
        "selected_lang": selected_lang,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "chat_history": chat_history,
        "languages": languages,
        "error": error,  # передаём ошибку, если была
        "FASTAPI_BASE_URL": settings.FASTAPI_BASE_URL, 
    })

@login_required
def clear_chat(request):
    try:
        # Удаляем все записи истории чатов для текущего пользователя
        ChatHistory.objects.filter(user=request.user).delete()

        # Перенаправляем пользователя обратно на главную страницу перевода
        return redirect('translate_text')
    except Exception as e:
        return HttpResponseServerError(f"Произошла ошибка: {str(e)}")
    

FASTAPI_BASE = getattr(settings, "FASTAPI_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

@csrf_exempt
def voice_proxy(request, path):
    """
    Простой прокси на FastAPI: /voice/<path> -> <FASTAPI_BASE>/<path>
    Пробрасывает метод, заголовки (без Host), тело/файлы, возвращает статус/контент.
    """
    url = f"{FASTAPI_BASE}/{path}"

    # базовые заголовки, уберём Host/Content-Length — их посчитает requests
    headers = {k: v for k, v in request.headers.items()
               if k.lower() not in {"host", "content-length"}}

    # Если у тебя используется JWT для авторизации между сервисами —
    # можно сюда добавить Authorization (если надо), например:
    # headers["Authorization"] = f"Bearer {<твой_токен>}"
    # Но если FastAPI эндпоинты публичные — не нужно.

    try:
        if request.method in ("POST", "PUT", "PATCH"):
            # Поддержим multipart/form-data (FormData с файлом)
            files = []
            for key, f in request.FILES.items():
                files.append((key, (f.name, f.read(), f.content_type or "application/octet-stream")))
            data = request.POST.dict() if request.POST else None

            resp = requests.request(
                method=request.method,
                url=url,
                headers=headers,
                data=data,
                files=files or None,
                timeout=60,
            )
        else:
            # GET/DELETE и пр. + query string
            resp = requests.request(
                method=request.method,
                url=url,
                headers=headers,
                params=request.GET.copy(),
                timeout=30,
            )

    except requests.RequestException as e:
        return JsonResponse({"error": "upstream_error", "detail": str(e)}, status=502)

    # Отдаём как есть
    dj = HttpResponse(resp.content, status=resp.status_code)
    # Пробросим важные заголовки
    for k, v in resp.headers.items():
        if k.lower() in {"content-type", "cache-control"}:
            dj[k] = v
    return dj