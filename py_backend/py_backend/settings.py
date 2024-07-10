"""
Django settings for py_backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from django.core.management.utils import get_random_secret_key
import os

AUTH_USER_MODEL = 'users.CustomUser'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ['*']

# Define for backend

MIN_LEN_USERNAME = 3
MIN_LEN_PASSWORD = 8
MAX_LEN_USERNAME = 25
MAX_LEN_EMAIL = 50
MAX_LEN_TEXT = 500
FORTY_TWO_UID = 'u-s4t2ud-92889d666741a2b0d333c0b63e74d6491194432da0c98a38a82560e58f9b0f83'
FORTY_TWO_SECRET = os.environ.get("FORTY_TWO_SECRET")
FORTY_TWO_REDIRECT_URI = 'https://127.0.0.1:8000/api/auth42/callback/'
LANG = ['en', 'fr', 'es']

# Application definition

INSTALLED_APPS = [
	'corsheaders',
	'daphne',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# 'django_extensions',
    'channels',
	'multiplayer',
	'users',
	'friends',
	'tournaments',
    'stats',
	'auth42',
]

ASGI_APPLICATION = 'py_backend.asgi.application'

CHANNEL_LAYERS = {
	"default": {
		 "BACKEND": "channels.layers.InMemoryChannelLayer"
		# "BACKEND": "channels_redis.core.RedisChannelLayer",
		# "CONFIG": {
		#     "hosts": [("127.0.0.1", 6379)],
		# },
	},
}

MIDDLEWARE = [
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'corsheaders.middleware.CorsMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'py_backend.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		# 'DIRS': [os.path.join(BASE_DIR, 'frontend', 'templates')],
  		'DIRS': [BASE_DIR / 'users/templates'], 
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

WSGI_APPLICATION = 'py_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
# 	"default": {
# 		"ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.postgresql"),
# 		"NAME": os.environ.get("SQL_DATABASE"),
# 		"USER": os.environ.get("SQL_USER", "user"),
# 		"PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
# 		"HOST": os.environ.get("SQL_HOST", "localhost"),
# 		"PORT": os.environ.get("SQL_PORT", "5432"),
# 	}
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
		"OPTIONS": {
			"min_length": MIN_LEN_PASSWORD,
		},
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
	{
		'NAME': 'users.validators.ContainsDigitValidator',
	},
	{
		'NAME': 'users.validators.ContainsSpecialCharValidator',
	},
	{
		'NAME': 'users.validators.ContainsUppercaseValidator',
	},
	{
		'NAME': 'users.validators.ContainsLowercaseValidator',
	},
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = "/staticfiles/"
# STATICFILES_DIRS = [
#     BASE_DIR / "frontend/static",  # Path to your "frontend" folder
# ]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = True # A Retirer
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
	"https://127.0.0.1:8000",
	"https://localhost:8000",
]

CSRF_TRUSTED_ORIGINS = [
	"https://127.0.0.1:8000",
	"https://localhost:8000",
]

ALLOWED_HOSTS = [
	"localhost",
	"127.0.0.1",
    "0.0.0.0"
]

CORS_ORIGIN_WHITELIST = [
	"https://127.0.0.1:8000",
	"https://localhost:8000",
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'backend.amos@gmail.com'
EMAIL_HOST_PASSWORD = 'hvqzjctapjxiijjf'
EMAIL_USE_TLS = True
