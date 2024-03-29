import logging
from datetime import timedelta
from pathlib import Path
import os
from corsheaders.defaults import default_headers
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Logging setup
logger = logging.getLogger(__name__)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'app': {
            'format': (
                '%(asctime)s [%(levelname)-8s] '
                '(%(module)s.%(funcName)s) %(message)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'app'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'D',
            'interval': 7,
            'backupCount': 1,
            'encoding': 'utf8',
            'filename': 'logs/debug.log',
            'formatter': 'app'
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console', 'file']},
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    }
}

# Secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-mw_n2-#0p-4p-asm7_f+sm8sck8bej&t7#jgcyn1z-ano(#mun')

#Google Cloud settings
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '.data/google_cloud_key.json')
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
GS_BUCKET_NAME = 'studyhub-static'
GS_DATA_BUCKET_NAME = os.environ.get('BUCKET_NAME', 'studyhub-data-dev')
GS_PROJECT_ID = 'studyhub-372200'

# Debug mode
DEBUG = os.environ.get('DEBUG', "True") == "True"

# Allowed hosts for request
ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOSTS', '*')]

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOW_HEADERS = list(default_headers) + [
    "x-api-key",
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_api_key',
    'corsheaders',
    'health_check',
    'health_check.db',
    'health_check.cache',
    'user',
    'deck',
    'user_action',
    'studyhub'
]

# API Setup
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

# ADFS
AUTH_ADFS = {
    'URL': os.environ.get('ADFS_URL', 'sso.university.innopolis.ru/'),
    'CLIENT_ID': os.environ.get('ADFS_CLIENT_ID', '02bdd68b-3508-40fa-aa30-c2b9e6f2f4c5'),
    'CLIENT_SECRET': os.environ.get('ADFS_CLIENT_SECRET', 'mK0gJz4Wq5gcQDOv2C59jjsJzNWCfqb91cgp5ltm')
}

# Moodle
MOODLE_API = {
    'URL': os.environ.get('MOODLE_URL', 'dev.moodle.innopolis.university/webservice/rest/server.php'),
    'TOKEN': os.environ.get('MOODLE_TOKEN', 'f1cc7bed428ef04b92943587e41a03af')
}

# AUTH setup
AUTH_USER_MODEL = 'user.User'

# JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework_api_key.permissions.HasAPIKey',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=100),
}

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'StudyHub API',
    'DESCRIPTION': 'Api for StudyHub',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

# Server settings
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

ROOT_URLCONF = 'studyhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'studyhub.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'studyhub_dev'),
        'USER': os.environ.get('DB_USER', 'diazzzu'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'pass1234'),
        'HOST': os.environ.get('DB_HOST', '0.0.0.0'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
DEFAULT_FILE_STORAGE = 'studyhub.storage.GoogleCloudMediaStorage'
STATICFILES_STORAGE = 'studyhub.storage.GoogleCloudStaticStorage'
STATIC_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
