import os

from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', default='some_key')

RUN_LOCAL_DEBUG = os.getenv('RUN_LOCAL_DEBUG', default=0)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = (os.getenv('ALLOWED_HOSTS', default='localhost')).split()

AUTH_USER_MODEL = 'users.User'

STATIC_URL = '/static_backend/'
MEDIA_URL = '/media_backend/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_backend')

if RUN_LOCAL_DEBUG:
    DEBUG = True
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_backend')]
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'foodgram_db',
            'USER': 'practicum',
            'PASSWORD': 'practicum',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_backend')
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE',
                                default='django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', default='mydatabase'),
            'USER': os.getenv('POSTGRES_USER', default='mydatabaseuser'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='mypassword'),
            'HOST': os.getenv('DB_HOST', default='db'),
            'PORT': os.getenv('DB_PORT', default='5432')
        }
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'colorfield',
    'api_foodgram.apps.ApiFoodgramConfig',
    'foodgram.apps.FoodgramConfig',
    'users.apps.UsersConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '500/minute',
        'anon': '100/minute',
    },
    'DEFAULT_PAGINATION_CLASS': ('api_foodgram'
                                 '.paginations.CustomPageNumberPagination'),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'HIDE_USERS': False,
    # https://djoser.readthedocs.io/en/latest/settings.html#serializers
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomDjoserUserCreateSerializer',
        'user': 'users.serializers.CustomDjoserUserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
}

MIDDLEWARE = [
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
        'DIRS': [],
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
