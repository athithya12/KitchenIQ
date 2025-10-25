import os
from pathlib import Path
import environ
import supertokens_python
from supertokens_python.recipe import session, emailpassword
from supertokens_python import get_all_cors_headers
from typing import List
from corsheaders.defaults import default_headers

# --- Initialization ---
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- CORE SETTINGS ---
SECRET_KEY = env('SECRET_KEY', default='django-insecure-fallback-key-for-local-dev-only')
DEBUG = False # True in development.py
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*']) 

# --- 1. INSTALLED APPLICATIONS ---
INSTALLED_APPS = [    
    'daphne',               # ASGI and Websockets
    
    # Core Django Apps (Minimal required for auth/sessions/admin)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'drf_yasg',             # API Documentation 
    'storages',             # S3/MinIO Integration
    'channels',             # WebSockets Framework
    'corsheaders',          # CORS
    'supertokens_python'    # Auth Service
]

# --- 2. MIDDLEWARE CONFIGURATION ---
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'supertokens_python.framework.django.django_middleware.middleware',
]

ROOT_URLCONF = 'kitcheniq.urls'

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

WSGI_APPLICATION = 'kitcheniq.wsgi.application'

# --- 3. DATABASE (Postgres) ---
DATABASES = {
    # Uses the DATABASE_URL environment variable from docker-compose
    'default': env.db(default='postgres://user:password@db:5432/kitcheniq')
}

# --- 4. CHANNELS (WebSockets via Redis) ---
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Uses the REDIS_URL environment variable
            "hosts": [env.str('REDIS_URL', default='redis://localhost:6379/0')],
        },
    },
}
ASGI_APPLICATION = 'kitcheniq.asgi.application'

# --- 5. SUPERTOKENS (Authentication) ---
supertokens_python.init(
    app_info=supertokens_python.InputAppInfo(
        app_name='KitchenIQ',
        api_domain=env.str('API_DOMAIN', default='http://localhost:8000'),
        website_domain=env.str('WEBSITE_DOMAIN', default='http://localhost:3000'),
    ),
    supertokens_config=supertokens_python.SupertokensConfig(
        connection_uri=env.str('SUPERTK_HOST', default='http://localhost:3567'),
    ),
    recipe_list=[
        session.init(), 
        emailpassword.init(),
    ],
    framework='django',
    mode='asgi'
)

# --- 6. STORAGE (S3/MinIO) ---
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', default='kitcheniq-media-bucket')
# Access keys/endpoints will be added in development.py and production config

# --- STANDARD DEFAULTS ---
TIME_ZONE = 'UTC'
USE_TZ = True
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- 6. CORS HEADERS CONFIGURATION ---
CORS_ORIGIN_WHITELIST = [
    "<YOUR_WEBSITE_DOMAIN>"
]
CORS_ALLOWED_ORIGINS = [env.str('WEBSITE_DOMAIN', default='http://localhost:3000')]
CORS_ALLOW_HEADERS: List[str] = list(default_headers) + [
    "Content-Type"
] + get_all_cors_headers()

CORS_ALLOW_CREDENTIALS = True