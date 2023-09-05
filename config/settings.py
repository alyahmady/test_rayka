from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

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


ADMINS = [tuple(admin.strip().split(";")) for admin in env.list("ADMINS", [])]


SECRET_KEY = env.str("SECRET_KEY")


FRONT_BASE_URL_NETLOC = (
    env.str("FRONT_BASE_URL_NETLOC")
    .replace("http://", "")
    .replace("https://", "")
    .strip(":/ ")
)
assert (
    FRONT_BASE_URL_NETLOC
), "`FRONT_BASE_URL_NETLOC` is required in a valid format (e.g. `raykatest.com`)"
FRONT_BASE_URL_SCHEME = (
    env.str("FRONT_BASE_URL_SCHEME", "https").replace("://", "").strip(":/ ")
)
assert FRONT_BASE_URL_SCHEME in (
    "https",
    "http",
), "`FRONT_BASE_URL_SCHEME` must be either `https` or `http`"
FRONT_URL = f"{FRONT_BASE_URL_SCHEME}://{FRONT_BASE_URL_NETLOC}"

BASE_URL_NETLOC = (
    env.str("BASE_URL_NETLOC")
    .replace("http://", "")
    .replace("https://", "")
    .strip(":/ ")
)
assert (
    BASE_URL_NETLOC
), "`BASE_URL_NETLOC` is required in a valid format (e.g. `api.raykatest.com`)"

BASE_URL_SCHEME = env.str("BASE_URL_SCHEME", "https").replace("://", "").strip(":/ ")
assert BASE_URL_SCHEME in (
    "https",
    "http",
), "`BASE_URL_SCHEME` must be either `https` or `http`"

ALLOWED_HOSTS = [BASE_URL_NETLOC.split(":")[0].strip("/:?& "), "localhost", "127.0.0.1"]
CSRF_TRUSTED_ORIGINS = list(
    set(
        [f"{BASE_URL_SCHEME}://{BASE_URL_NETLOC}"]
        + env.list("CSRF_TRUSTED_ORIGINS", [])
    )
)

CORS_ALLOWED_ORIGINS = [f"{BASE_URL_SCHEME}://{BASE_URL_NETLOC}", FRONT_URL]
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", True)
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", False)


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "corsheaders",
    "rest_framework",
    # local
    "apps.devices.apps.DevicesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("TIME_ZONE", "UTC")

USE_I18N = True

USE_TZ = True

LOG_DIR = BASE_DIR / env.str("LOGS_DIRECTORY", "logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

DJANGO_DEBUG_LOG_FILE_NAME = env.str("DJANGO_DEBUG_LOG_FILE_NAME", "django.log")
DJANGO_DEBUG_LOG_FILE = LOG_DIR / DJANGO_DEBUG_LOG_FILE_NAME
Path(DJANGO_DEBUG_LOG_FILE).touch(exist_ok=True)

LOGGER_NAME = "test_rayka_logger"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "\n\nTime: {asctime}\nFile: {pathname}\nModule: {module}"
            "\nFunction: {funcName}\nDetails: {message}\nArgs: {args}\n",
            "style": "{",
        },
        "simple": {"format": "\n{levelname} {asctime} - {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        LOGGER_NAME: {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": DJANGO_DEBUG_LOG_FILE,
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 100,
            "backupCount": 5,
        },
    },
    "loggers": {
        LOGGER_NAME: {
            "handlers": [LOGGER_NAME, "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


API_PREFIX = env.str("API_PREFIX", "api").strip("/ ")
assert API_PREFIX, "`API_PREFIX` is required"


AWS_REGION_NAME = env.str("AWS_REGION_NAME")

AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")

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
