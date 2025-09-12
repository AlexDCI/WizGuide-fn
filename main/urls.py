from django.urls import path, re_path
from . import views

urlpatterns = [
    # прокси
    re_path(r'^voice/(?P<path>.*)$', views.voice_proxy, name='voice_proxy'),

    # алиасы под фронтовые пути
    path('api/token/me', views.issue_token, name='issue_token_api'),
    path('api/save-speech', views.save_speech_result, name='save_speech_api'),

    # остальное
    path('', views.main_page, name='main'),
    path('translate/', views.translate_text, name='translate_text'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('token/me', views.issue_token, name='issue_token'),
    path('save-speech', views.save_speech_result, name='save_speech'),
]
