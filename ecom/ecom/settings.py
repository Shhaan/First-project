from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-#spx(8i(m_@n#!h^r-h@%y0+r44ia2a=bt_8#_h52j6hun8gz3"

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "adminhome",
    "usermain",
    "admincrud",
    "productdetail",
    "userprofile",
    "userorder",
    "paypal.standard.ipn",
    "crispy_forms",
]


CRISPY_TEMPLATE_PACK = "bootstrap4"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "shanmohamme.123@gmail.com"
EMAIL_HOST_PASSWORD = "nfsq ywqv lwva zlod"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecom.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "adminhome", "template"),
            os.path.join(BASE_DIR, "usermain", "template"),
            os.path.join(BASE_DIR, "admincrud", "template"),
            os.path.join(BASE_DIR, "productdetail", "template"),
            os.path.join(BASE_DIR, "userprofile", "template"),
            os.path.join(BASE_DIR, "userorder", "template"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ecom.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ecomdb",
        "USER": "postgres",
        "PASSWORD": "sql#786",
        "HOST": "localhost",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "adminhome", "static"),
    os.path.join(BASE_DIR, "usermain", "static"),
    os.path.join(BASE_DIR, "admincrud", "static"),
    os.path.join(BASE_DIR, "productdetail", "static"),
    os.path.join(BASE_DIR, "userprofile", "static"),
    os.path.join(BASE_DIR, "userorder", "static"),
]

AUTH_USER_MODEL = "usermain.Users"

STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


PAYPAL_RECEIVER_EMAIL = "sb-uqmtx28976968@business.example.com"
PAYPAL_TEST = True
