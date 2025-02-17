import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from users.models import CustomUser  # Используем кастомную модель пользователя
from .models import ChatHistory
from .services import translate_text_api, generate_comment_api, save_chat_to_db, get_user_chat_history
from .views import translate_text
from django.test import TestCase
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse


# Устанавливаем переменную окружения для Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'wiz_guide_fn.settings'

# Импортируем Django, после того как установили настройки
import django
django.setup()

# Пример теста для перевода текста через API
@patch("main.services.openai.ChatCompletion.create")
def test_translate_text_api(mock_create):
    mock_create.return_value = {
        "choices": [{"message": {"content": "Привет"}}]
    }

    translation = translate_text_api("English", "Russian", "Hello")
    
    assert translation == "Привет"
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a translator. Translate from English to Russian."},
            {"role": "user", "content": "Hello"}
        ]
    )


# Пример теста для генерации комментария через API
@patch("main.services.openai.ChatCompletion.create")
def test_generate_comment_api(mock_create):
    mock_create.return_value = {
        "choices": [{"message": {"content": "This is a simple greeting."}}]
    }

    comment = generate_comment_api("Russian", "Привет", "Provide a short comment about the translation.")
    
    assert comment == "This is a simple greeting."
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant providing explanations. Respond in Russian."},
            {"role": "user", "content": "Translation: Привет. Provide a short comment about the translation."}
        ]
    )


# Пример теста для сохранения чатов в базу данных
@pytest.mark.django_db
def test_save_chat_to_db():
    # Создаем реального пользователя CustomUser
    user = CustomUser.objects.create_user(username='testuser', password='password')
    input_text = "Hello"
    translated_text = "Привет"
    comment = "A simple greeting."

    save_chat_to_db(user, input_text, translated_text, comment)

    chat_history = ChatHistory.objects.first()
    assert chat_history.user == user
    assert chat_history.input_text == input_text
    assert chat_history.translated_text == translated_text
    assert chat_history.comment == comment


# Пример теста для получения истории чатов пользователя
@pytest.mark.django_db
def test_get_user_chat_history():
    # Создаем реального пользователя CustomUser
    user = CustomUser.objects.create_user(username='testuser', password='password')
    ChatHistory.objects.create(user=user, input_text="Hello", translated_text="Привет", comment="Test")
    ChatHistory.objects.create(user=user, input_text="How are you?", translated_text="Как дела?", comment="Test 2")
    
    history = get_user_chat_history(user)
    
    assert len(history) == 2
    assert history[0].input_text == "How are you?"
    assert history[1].input_text == "Hello"


# Пример теста для views.py: translate_text (обработка запроса на перевод)
class TranslateTextViewTest(TestCase):
    @pytest.mark.django_db
    def test_translate_text_get(self):
        # Создаем реального пользователя CustomUser
        user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        
        response = self.client.get(reverse('translate_text'))
        assert response.status_code == 200
        assert 'translations' in response.context
        assert 'languages' in response.context


    @pytest.mark.django_db
    @patch("main.views.translate_text_api")
    @patch("main.views.generate_comment_api")
    def test_translate_text_post(self, mock_generate_comment, mock_translate):
        mock_translate.return_value = "Привет"
        mock_generate_comment.return_value = "A simple greeting."

        # Создаем реального пользователя CustomUser
        user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        
        response = self.client.post(reverse('translate_text'), {
            'text': 'Hello',
            'source_lang': 'English',
            'target_lang': 'Russian',
            'comment_request': 'Explain this translation.'
        })
        
        # Проверяем, что данные были сохранены в базе
        chat_history = ChatHistory.objects.first()
        assert chat_history.input_text == "Hello"
        assert chat_history.translated_text == "Привет"
        assert chat_history.comment == "A simple greeting."
        
        # Проверяем редирект с актуальными параметрами
        assert response.status_code == 302
        assert "source_lang=English" in response.url
        assert "target_lang=Russian" in response.url


