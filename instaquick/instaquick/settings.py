"""
InstaQuick project settings
Covers: Food Delivery + Grocery Delivery web app
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# SECURITY
# ---------------------------------------------------------------------------
SECRET_KEY = "django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYMENT"
DEBUG = True
ALLOWED_HOSTS = ["*"]  # restrict this in production

# ---------------------------------------------------------------------------
# APPLICATION DEFINITION
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # our apps
    "accounts",
    "food",
    "grocery",
    "orders",
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

ROOT_URLCONF = "instaquick.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # global templates folder (base.html, navbar, footer, home, login, register)
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # makes cart item-count available on every page (navbar badge)
                "orders.context_processors.cart_summary",
                # makes {{ GOOGLE_MAPS_API_KEY }} available on every page
                "orders.context_processors.google_maps_key",
            ],
        },
    },
]

WSGI_APPLICATION = "instaquick.wsgi.application"

# ---------------------------------------------------------------------------
# DATABASE  -> this is what stores customer/order/product data and is what
# shows up inside /admin (the "django-administration" database screen)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# STATIC / MEDIA
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# AUTH REDIRECTS
# ---------------------------------------------------------------------------
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "accounts:login"

# ---------------------------------------------------------------------------
# THIRD-PARTY KEYS  (get your own free/test keys and put them here)
# Google Maps: https://console.cloud.google.com/  (enable Maps JavaScript API)
# Razorpay (UPI/Card/COD test mode): https://dashboard.razorpay.com/
# ---------------------------------------------------------------------------
GOOGLE_MAPS_API_KEY = "PUT_YOUR_GOOGLE_MAPS_API_KEY_HERE"
RAZORPAY_KEY_ID = "PUT_YOUR_RAZORPAY_TEST_KEY_ID_HERE"
RAZORPAY_KEY_SECRET = "PUT_YOUR_RAZORPAY_TEST_KEY_SECRET_HERE"
