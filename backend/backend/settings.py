"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# this is for the .env decoupling
from decouple import config, Csv

import dj_database_url
#here importing os and setting up templates so django can recongnize the index.html


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='unsafe-default-key')  # Provide a default for safety

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)  # Convert DEBUG to a boolean

# Load SECRET_KEY and DEBUG from the .env file


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #//
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    
    #// django app
    'employees',
    'appointments',
    #for a server running in a different port than the main file
    'corsheaders',
    'django_celery_results',
]

#//This is a set up in the customAuth_backends.py that allows to use the authenticate
#//function to check against employeeId instead of the default username

# AUTHENTICATION_BACKENDS = [
#     'backend.customAuth_backends.EmployeeIDBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]

#//
# Allow specific origins (your frontend URL)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["http://localhost:5173","https://careconnected-frontend-v1-0.onrender.com",]  # We add your frontend URL here.
CSRF_TRUSTED_ORIGINS = ['http://localhost:5173', "https://careconnected-frontend-v1-0.onrender.com",]  # We add your frontend URL here.



SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

#//

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


DJOSER = {
    'USER_ID_FIELD': 'employee_id',  # Set employee_id as the user ID field
    'LOGIN_FIELD': 'employee_id',  # Use employee_id for login
}

AUTH_USER_MODEL = 'employees.Employee'

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost,https://careconnected-backend-v1-0.onrender.com,careconnected-backend-v1-0.onrender.com', cast=Csv())



# ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

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
#//

MIDDLEWARE = [
    #
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #//
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

# 
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Ensure this points to your static directory
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Sending messages logic
# config = Config('/app/.env')

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# Celery Settings
# Celery Configuration for dev
# CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the message broker
#celerey with redis on docker
##UNCOMMENT IF RUNNING LOCALLY AND COMMENT FOR PRODUCTION
# CELERY_BROKER_URL = 'redis://redis:6379/0'

CELERY_ACCEPT_CONTENT = ['json']                # Accept JSON messages
CELERY_TASK_SERIALIZER = 'json'                 # Serialize tasks as JSON
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Store results in Redis

# Celery Results Backend for dev(optional, can be set to that or just the local host port)
##UNCOMMENT IF RUNNING LOCALLY AND COMMENT FOR PRODUCTION
# CELERY_RESULT_BACKEND = 'django-db'

#for production
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379')

# CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
# CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')