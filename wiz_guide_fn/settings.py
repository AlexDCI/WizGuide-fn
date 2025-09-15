from pathlib import Path
import os
from dotenv import load_dotenv

# Загружаем .env переменные
load_dotenv()

# 🔑 OpenAI API KEY (если используется)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8001")

# 📁 Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "::1", "192.168.178.27"]

CSRF_TRUSTED_ORIGINS = [
    "http://192.168.178.27:8000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
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

    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

VOICE_JWT_SECRET = os.getenv("VOICE_JWT_SECRET", SECRET_KEY)  # общий секрет с FastAPI

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

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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


# 🧪 Для тестов
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# 🛠 Авто-ключи
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

