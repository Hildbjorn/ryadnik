"""
Настройки проекта
Copyright (c) 2025 Artem Fomin
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Построение пути внутри проекта следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Построение пути к файлу .env
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Секретный ключ приложения
SECRET_KEY = os.environ.get('SECRET_KEY')

# Режим отладки
DEBUG = os.environ.get('DEBUG', '').lower() in ['true', '1', 'yes']

# Доступные хосты
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# Определение приложений
INSTALLED_APPS = [
    # Приложения по умолчанию ---------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Сторонние служебные приложения --
    'captcha',
    'django_htmx',
    'django_bootstrap5',
    'sass_processor',
    'widget_tweaks',
    # Приложения данного приложения ---
    'common',
    'users',
    'home',
    'tasks',
    # ---------------------------------
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'ryadnik.urls'

# Шаблоны Django
TEMPLATES_BASE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_BASE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Путь к настройкам wsgi
WSGI_APPLICATION = 'ryadnik.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.environ.get('DATABASE_NAME'),
    }
}

# Проверка пароля
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

# Использование класса Profile
AUTH_USER_MODEL = 'users.Profile'
# Перенаправление на домашний URL после входа
LOGIN_REDIRECT_URL = '/'

# Интернационализация
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Статические файлы (CSS, JavaScript, Img, Fonts)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATICFILES_DIRS = [
    BASE_DIR.joinpath('static'),
]

STATIC_ROOT = BASE_DIR.joinpath('staticfiles')

STATIC_URL = '/static/'

# Папка итогового хранения css и js
SASS_PROCESSOR_ROOT = STATIC_ROOT

# Настройки Django-Bootstrap
BOOTSTRAP5 = {
    "javascript_url": {
        "url": "/static/bootstrap/js/bootstrap.bundle.min.js",
    },
}

# Настройки иконок Bootstrap в Django/
DJANGO_ICONS = {
    "DEFAULT": {
        "renderer": "django_icons_bootstrap_icons.BootstrapIconRenderer"
    }
}

# Медиафайлы (фото, презентации и т.д.)
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR.joinpath('media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки Captcha
CAPTCHA_LENGTH = 5
CAPTCHA_FONT_SIZE = 26
# CAPTCHA_IMAGE_SIZE = (75, 50)
CAPTCHA_2X_IMAGE = True
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

# Настройки электронной почты vniicentr.ru
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'НИОКРИД <afomin@vniicentr.ru>'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', '').lower() in [
    'true', '1', 'yes']
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', '').lower() in [
    'true', '1', 'yes']

# Настройки Telegtam, с которого будут отправляться сообщения
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# Список пользователей для рассылки через Telegram по умолчанию
USERS_TELEGRAM_ID = os.getenv('USERS_TELEGRAM_ID')
if USERS_TELEGRAM_ID:
    USERS_TELEGRAM_ID = [int(id) for id in USERS_TELEGRAM_ID.split(',')]
else:
    USERS_TELEGRAM_ID = []
