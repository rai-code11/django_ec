from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# "*"に設定することで、すべてのホストを許可
ALLOWED_HOSTS = ["*"]

# mediaファイルの設定
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
