"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# settings.py

from pathlib import Path
import os
from decouple import config, Csv
import dj_database_url
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = config('SECRET_KEY', default='unsafe-default-key')  # Ensure to set a strong secret key in production
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost,careconnected-backend-v1-0.onrender.com,careconnected-frontend-v1-0.onrender.com',
    cast=Csv()
)

# SECURITY PROXY SSL HEADER
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# APPLICATION DEFINITION
INSTALLED_APPS = [
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_celery_results',
    
    # Your Django apps
    'employees',
    'appointments',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',            # Must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',         # Retain if needed for other forms
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

# TEMPLATES CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Ensure this points to your templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required by Django admin
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# DATABASE CONFIGURATION
DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL', default='sqlite:///db.sqlite3'))
}

# PASSWORD VALIDATION
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

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Ensure this points to your static directory
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CUSTOM USER MODEL
AUTH_USER_MODEL = 'employees.Employee'

# REST FRAMEWORK CONFIGURATION
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# SIMPLE JWT CONFIGURATION
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Adjust as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,  # Enable blacklisting after rotation
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
}

# CORS SETTINGS
CORS_ALLOW_CREDENTIALS = True  # Allow cookies to be sent
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",                      # Local Frontend (Vue)
    "http://localhost:3000",                      # Alternative Frontend (if applicable)
    "https://careconnected-frontend-v1-0.onrender.com",  # Production Frontend
]

# LOGGING CONFIGURATION
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Twilio Configuration
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# CELERY CONFIGURATION
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
# For Production (Commented Out)
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379')

# For local development comment out
# Redis as the message broker
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  
# CELERY_RESULT_BACKEND = 'django-db'
