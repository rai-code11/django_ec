from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [".herokuapp.com"]  # herokuapp.comドメインを許可


STORAGES = {
    # 静的ファイル
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    # 画像アップロード
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
}

# ImageKitがサムネイルを保存する場所としてCloudinaryを明示的に指定
IMAGEKIT_DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
