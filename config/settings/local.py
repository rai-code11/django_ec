from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# "*"に設定することで、すべてのホストを許可
ALLOWED_HOSTS = ["*"]

# ローカル環境でもwhitenoiseを使う設定
INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
