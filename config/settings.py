from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

TEST_RUNNER = "apps.devices.tests.NoDatabaseTestRunner"

DEBUG = env.bool("DEBUG", None)

if DEBUG is None:
    env_file_path = BASE_DIR / ".env"
    assert env_file_path.exists(), (
        "No environment file found. "
        "Please create the following file "
        "(based on `./.env.example`): `./.env`"
    )
    env.read_env(env_file_path)

    DEBUG = env.bool("DEBUG", False)

TESTING = env.bool("TESTING_MODE", False)

AWS_DEPLOY_REGION = env.str("AWS_DEPLOY_REGION", "eu-north-1")

ADMINS = [tuple(admin.strip().split(";")) for admin in env.list("ADMINS", [])]

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [f".{AWS_DEPLOY_REGION}.amazonaws.com", "localhost", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [f"https://*.{AWS_DEPLOY_REGION}.amazonaws.com"]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    # 3rd party
    "rest_framework",
    # local
    "apps.devices.apps.DevicesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = env.str("WSGI_APPLICATION", "config.wsgi.application")

LANGUAGE_CODE = "en-us"
TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = False
USE_TZ = True

LOGGER_NAME = "test_rayka_logger"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "\n\nTime: {asctime}\nFile: {pathname}\nModule: {module}"
            "\nFunction: {funcName}\nDetails: {message}\nArgs: {args}\n",
            "style": "{",
        }
    },
    "handlers": {
        LOGGER_NAME: {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        LOGGER_NAME: {"handlers": [LOGGER_NAME], "level": "DEBUG", "propagate": True},
    },
}


API_PREFIX = env.str("API_PREFIX", "api").strip("/ ")
assert API_PREFIX, "`API_PREFIX` is required"

API_VERSION = env.str("API_VERSION", "v1").strip("/ ")
assert (
    API_VERSION.startswith("v") and API_VERSION[1:].isdigit()
), "`API_VERSION` must start with `v` and be followed by a number (e.g. `v1`)"

PROJECT_KEY = env.str("PROJECT_KEY", "rayka_test")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.ScopedRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "1000/day",
        "device_create": "45/minute",
        "device_retrieve": "45/minute",
    },
}

if DEBUG:
    for key in REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]:
        REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"][key] = "60/minute"


DDB_TABLE_READ_CAPACITY_UNITS = env.int("DDB_TABLE_READ_CAPACITY_UNITS", 5)
DDB_TABLE_WRITE_CAPACITY_UNITS = env.int("DDB_TABLE_WRITE_CAPACITY_UNITS", 5)


if TESTING:
    # Useless. It's just for the sake of testing.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
