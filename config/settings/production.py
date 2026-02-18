from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [".herokuapp.com"]  # herokuapp.comドメインを許可

# 本番環境用のメール設定
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_HOST_USER = "apikey"
# ここにapi-keyを入れる
EMAIL_HOST_PASSWORD = env("SENDGRID_API_KEY", default="")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "hirai.fpchr064@gmail.com"


if not EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"


# デバック処理
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        # 500エラーのTracebackを確実に出す
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
