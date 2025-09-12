from django.urls import path, re_path
from . import views

urlpatterns = [
    # прокси
    path('api/token/me', views.issue_token),
    path('api/save-speech', views.save_speech_result),
    re_path(r'^voice/(?P<path>.*)$', views.voice_proxy),

    # остальное
    path('', views.main_page, name='main'),
    path('translate/', views.translate_text, name='translate_text'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('clear_chat/', views.clear_chat, name='clear_chat'),
    path('token/me', views.issue_token, name='issue_token'),
    path('save-speech', views.save_speech_result, name='save_speech'),
]
