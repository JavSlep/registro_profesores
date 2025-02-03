import os
from pathlib import Path
from django.urls import reverse_lazy
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# FVS modifica clase usuario
AUTH_USER_MODEL = 'usuario.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
""" CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000/'] """

""" SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer' """
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "crispy_forms",
    "crispy_bootstrap5",
    'django_dump_load_utf8',
    'import_export',
    'apps.utilidades',
    'apps.usuario',
    'captcha',
    'apps.profesores',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

ROOT_URLCONF = 'infraslep.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'infraslep.wsgi.application'

# FVS Activar Alertas
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
""" STATIC_ROOT = os.path.join(BASE_DIR, 'static/') """
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# fvs expira la seccion utilizando pip install django-session-timeout
SESSION_EXPIRE_SECONDS = 1500 #600 equivalen a 10 minutos
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# FVS CONFIGURACION RECAPTCHA
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# fvs configura parametros para envio de correos
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_CHARSET= config('DEFAULT_CHARSET')

JWT_SECRET = SECRET_KEY  # use settings secret key for JWT secret
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 86400  # 86400 token expiring time in seconds let's assign one day

# fvs para redireccionar una vez logeado Y DESLOGEADO
LOGIN_REDIRECT_URL= reverse_lazy('mis_entidades')
LOGOUT_REDIRECT_URL= reverse_lazy('mis_entidades')

X_FRAME_OPTIONS = 'SAMEORIGIN'

# fvs CRISPY
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

if DEBUG == False:
    CSRF_TRUSTED_ORIGINS = [
        'https://app.infraslep.cl',
        'http://app.infraslep.cl',  # Si usas HTTP en algún entorno
    ]
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Lax'    
    SECURE_CROSS_ORIGIN_OPENER_POLICY=True
    SESSION_COOKIE_SECURE=True
    URL_DOMINIO = 'http://45.236.129.27:80'
else:       
    URL_DOMINIO = 'http://127.0.0.1:8000'
    SECURE_CROSS_ORIGIN_OPENER_POLICY=False
    SESSION_COOKIE_SECURE=False
    