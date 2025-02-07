# main/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),  # Главная страница
    # path("chat/", views.chat_with_openai, name="chat_with_openai"),
    path('translate/', views.translate_text, name='translate_text'),
    path('about/', views.about, name='about'),  # Для страницы About
    path('contact/', views.contact, name='contact'),  # Для страницы Contact
]