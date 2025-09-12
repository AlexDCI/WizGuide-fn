# main/urls.py

from django.urls import path, re_path
from . import views

urlpatterns = [
    # ПРОКСИ НА FASTAPI
    re_path(r'^voice/(?P<path>.*)$', views.voice_proxy, name='voice_proxy'),

    path('', views.main_page, name='main'),  # Главная страница
    # path("chat/", views.chat_with_openai, name="chat_with_openai"),
    path('translate/', views.translate_text, name='translate_text'),
    path('about/', views.about, name='about'),  # Для страницы About
    path('contact/', views.contact, name='contact'),  # Для страницы Contact
    path('clear_chat/', views.clear_chat, name='clear_chat'),  # Очистка чата
    path('token/me', views.issue_token, name='issue_token'),
    path('save-speech', views.save_speech_result, name='save_speech'),
]