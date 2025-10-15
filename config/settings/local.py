from .base import *


environ.Env.read_env(env_file=str(BASE_DIR) + "/.env")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ["*"]  # "*"に設定する

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
        "TIME_ZONE": "Asia/Tokyo",
    }
}

INSTALLED_APPS.insert(0, "whitenoise.runserver_nostatic")
