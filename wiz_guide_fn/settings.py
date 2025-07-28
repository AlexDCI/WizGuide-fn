from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем .env переменные
load_dotenv()

# 🔑 OpenAI API KEY (если используется)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 📁 Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY')

# 🔧 Режим разработки
DEBUG = True

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost").split(",")

# 🧩 Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'users',  # используем только как модель пользователя

    # Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Дополнительно
    'django_extensions',
]

# 🧱 Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Для статики в проде

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'wiz_guide_fn.urls'

# 📐 Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # 🔑 важно для allauth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wiz_guide_fn.wsgi.application'

# 🗄️ База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'wizguide_bd'),
        'USER': os.getenv('POSTGRES_USER', 'wizguide_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'supersecurepassword'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# 🔐 Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 👤 Пользовательская модель
AUTH_USER_MODEL = 'users.CustomUser'

# 🌐 Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 🖼️ Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 🔑 Авторизация и редиректы
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 🧠 Django Allauth
SITE_ID = int(os.getenv("SITE_ID", 1))

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
    'django.contrib.auth.backends.ModelBackend',  # Стандартный backend
]

# ⚙️ Настройки allauth
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # Можно "optional" или "mandatory"

# 🌐 Google OAuth
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}
<<<<<<< HEAD
from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# open AI KEY sttings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True #os.getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')  # Преобразуем строку в булевое значение

# ALLOWED_HOSTS = ['167.71.34.6', 'localhost', '127.0.0.1'] # host for production

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'main',
    'users',

    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',  # для социальных аккаунтов
    'allauth.socialaccount.providers.google',  # Для Google

    'django_extensions',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'wiz_guide_fn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [ BASE_DIR / 'templates' ],
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,  # Включаем дебаг-режим
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            
            ],
        },
    },
]



WSGI_APPLICATION = 'wiz_guide_fn.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'wizguide_bd'),
        'USER': os.getenv('POSTGRES_USER', 'wizguide_user'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'supersecurepassword'),

        'HOST': os.getenv('DB_HOST', 'localhost'),  # Подключаемся к контейнеру db

        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Authentication for user accounts
AUTH_USER_MODEL = 'users.CustomUser'

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Добавляем путь к статическим файлам
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Django будет копировать все файлы сюда при collectstatic

# # Директория на вашем сервере, где будут собираться статические файлы
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# Если вы хотите собирать статические файлы в одну папку для продакшн, укажите:
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Маршрут для авторизации пользователей
LOGIN_URL = '/users/require-login/'

SITE_ID = int(os.getenv("SITE_ID", 1))


TEST_RUNNER = 'django.test.runner.DiscoverRunner'


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth backend
    'django.contrib.auth.backends.ModelBackend',  # стандартный backend
]


# Настройки для Google OAuth2 с django-allauth
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


LOGIN_REDIRECT_URL = '/'  # Куда перенаправлять после входа
LOGOUT_REDIRECT_URL = '/'  # Куда после выхода

# Новый формат настроек django-allauth
ACCOUNT_LOGIN_METHODS = {'username', 'email'}  # Разрешает вход по email и username
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']  # Обязательные поля при регистрации
ACCOUNT_EMAIL_VERIFICATION = "none"  # Можно изменить на "optional" или "mandatory"


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True
    }
}
=======

# 🧪 Для тестов
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# 🛠 Авто-ключи
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
>>>>>>> temporary-branch
