"""
Django sozlamalari — Dunyo shaharlari ma'lumotnomasi.

Maxfiy va muhitga bog'liq qiymatlar `.env` faylidan o'qiladi (namuna uchun
`.env.example` ga qarang). `.env` bo'lmasa, loyiha ishlab chiqish rejimida
xavfsiz standart qiymatlar bilan ishlaydi.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    """`.env` dagi "1/true/yes/on" qiymatlarini bool ga aylantiradi."""
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default):
    raw = os.getenv(name)
    if not raw:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


# ---------------------------------------------------------------- xavfsizlik

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-e7k1b$tzqrb$)2f+js(@9=+85b%8bm(-ekh09f(^@(%%-)65b0",
)

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "[::1]"])

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", [])

if not DEBUG:
    # Ishlab chiqarish (production) rejimida himoya standart holda yoqiladi.
    # HTTPS'siz tarqatishda `.env` da DJANGO_HTTPS_ONLY=False qo'ying.
    https_only = env_bool("DJANGO_HTTPS_ONLY", True)

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_HTTPONLY = True
    X_FRAME_OPTIONS = "DENY"

    SESSION_COOKIE_SECURE = https_only
    CSRF_COOKIE_SECURE = https_only
    SECURE_SSL_REDIRECT = https_only

    SECURE_HSTS_SECONDS = int(os.getenv("DJANGO_HSTS_SECONDS", "31536000")) if https_only else 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = https_only
    SECURE_HSTS_PRELOAD = https_only

    # Reverse-proxy (nginx, Traefik) orqasida ishlaganda yoqing.
    if env_bool("DJANGO_BEHIND_PROXY", False):
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# ---------------------------------------------------------------- ilovalar

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",  # Swagger UI fayllari lokal (CDN kerak emas)

    "cities.apps.CitiesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cityproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cityproject.wsgi.application"
ASGI_APPLICATION = "cityproject.asgi.application"


# ---------------------------------------------------------------- baza

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("DJANGO_DB_NAME", "db.sqlite3"),
    }
}


# ---------------------------------------------------------------- autentifikatsiya

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ---------------------------------------------------------------- mahalliylashtirish

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------- statik fayllar

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------- REST API

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # O'qish hamma uchun ochiq; yozish uchun tizimga kirish va ruxsat kerak.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Dunyo shaharlari API",
    "DESCRIPTION": (
        "Shaharlar va mamlakatlar ma'lumotnomasining REST API'si. "
        "O'qish (GET) hamma uchun ochiq, o'zgartirish uchun tizimga kirish kerak."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    # Interfeys fayllari loyihaning o'zidan beriladi - internetsiz ham ochiladi.
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}
