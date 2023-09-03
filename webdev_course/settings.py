import os
from pathlib import Path
from .utils import get_git_version

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Версия проекта
PROJECT_VERSION = '1.0.0'

# Версия проекта для локальной разработки
VERSION = get_git_version()

# Настройки безопасности
SECRET_KEY = 'django-insecure-r&r9qi8%dem9bq0)y5$epsp@2aa@loj806^o0%cag$%#2l$09j'
DEBUG = True
ALLOWED_HOSTS = ['*']


# Базовые приложения (пререквизитные)
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Приложения проекта
PROJECT_APPS = [
    'core',
    'students',
    'teachers'
]

# Общий список установленных приложений
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS


# Промежуточное ПО (middleware) для обработки запросов
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Определение корневого URL-конфига
ROOT_URLCONF = 'webdev_course.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webdev_course.context_processors.current_year',
                'webdev_course.context_processors.project_version',
            ],
        },
    },
]

# Настройки WSGI
WSGI_APPLICATION = 'webdev_course.wsgi.application'

# Настройки базы данных (используется SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Настройки валидации паролей
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


# Настройки интернационализации
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Настройки статических файлов
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'core/static'),
    os.path.join(BASE_DIR, 'students/static'),
    os.path.join(BASE_DIR, 'teachers/static'),
]


# Тип поля для автоматического ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Настройки медиафайлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
