"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import socket


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(q-!_5fqibje93(j+8*3=y@lwz*k!!3h1m@zx*u1t*4uk26xc&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# test
# newly added be developer
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", 'https')

ADMINS = [('carlington', 'carlingtonpalmer@gmail.com')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'crispy_forms',

    # custom
    'users',
    'reset_password',
    'request',
    'contact_us',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', #whitenoise heroku
]





ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#     'ENGINE': 'django.db.backends.postgresql_psycopg2',
#     'NAME': 'd69o1gq0feaals',
#     'USER': 'qictcmjehvuqvz',
#     'PASSWORD': 'e3369e5a2099348a2d78a7ac7a7ef7aeda29b81e7fd81e57a8088ecf0c2b8b46',
#     'HOST': 'ec2-3-222-150-253.compute-1.amazonaws.com',
#     'PORT': '5432',
#     }
# }

host_name = socket.gethostname()
# check it debug or live

# if 'Carlingtons-MBP.local' == host_name:
# if 'localhost' in ALLOWED_HOSTS:
print('Local')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# else:
#     print('Boo yah!!!, We on Heroku')
#     DATABASES = {
#         'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd69o1gq0feaals',
#         'USER': 'qictcmjehvuqvz',
#         'PASSWORD': 'e3369e5a2099348a2d78a7ac7a7ef7aeda29b81e7fd81e57a8088ecf0c2b8b46',
#         'HOST': 'ec2-3-222-150-253.compute-1.amazonaws.com',
#         'PORT': '5432',
#         }
#     }
        


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Jamaica'# previous value UTC changed date 08/16/2020

USE_I18N = True

USE_L10N = True

USE_TZ = False #set to false to get local time

# DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/' 

STATIC_ROOT = os.path.join(BASE_DIR,'static')
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' #heroku

""" developer added code """ 

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # <-- And here
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ]
}

# this is linked to serializer
REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER':
    'reset_password.serializers.ResetPasswordSerializer',
}




# if 'Carlingtons-MBP.local' == host_name:

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tuglife47@gmail.com'
EMAIL_HOST_PASSWORD = 'dztztiicexmisaea'
DEFAULT_FROM_EMAIL = 'App Dev <tuglife47@gmail.com>'

    

# else:

#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = 'smtp.gmail.com'
#     EMAIL_USE_TLS = True
#     EMAIL_PORT = 587
#     EMAIL_HOST_USER = 'teamappdev2019@gmail.com'
#     EMAIL_HOST_PASSWORD = 'bwpuqefzvcuztvgg'
#     DEFAULT_FROM_EMAIL = 'APP Dev<teamappdev2019@gmail.com>'



 # bootstrap 4 set default
CRISPY_TEMPLATE_PACK = 'bootstrap4'
COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', True) # this to fix 500 error for reset password when clicked

