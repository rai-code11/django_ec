from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]  # "*"に設定する


INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")
