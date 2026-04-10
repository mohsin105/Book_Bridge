from pathlib import Path
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'users.User'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    'djoser',
    'django_filters',
    "corsheaders",
    'drf_yasg',
    'users',
    'books',
    'borrow',
    "api",
    'core',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'book_bridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'book_bridge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Postgreql - Local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'book_bridge',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}



"""  Authentication settings ---------->           """

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),    # here, JWT is the prefix of your jwt tokens
   "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
}

DJOSER = {
    'EMAIL_FRONTEND_PROTOCOL':config('FRONTEND_PROTOCOL') ,
    'EMAIL_FRONTEND_DOMAIN': config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME':'Bookbridge' ,
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}/',
    'SERIALIZERS': {
            'user_create':'users.serializers.UserCreateSerializer',
			'current_user': 'users.serializers.UserSerializer',
		},
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

""" Email Settings ------>        """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST',default='')
EMAIL_PORT = config('EMAIL_PORT',cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS',cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER',default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD',default='') 



""" Media & Static related settings -------->   """

STATIC_URL = 'static/'

MEDIA_URL='/media/'
MEDIA_ROOT= BASE_DIR / 'media'


BACKEND_URL = 'http://127.0.0.1:8000'


"""Swagger Settings --------->        """

SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description':'Enter Your JWT token in the format:`JWT <Your_token>`'
      }
   }
}