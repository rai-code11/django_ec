from django.db import models
from cloudinary.utils import cloudinary_url
import time

# Create your models here.


class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.AutoField("id", primary_key=True)
    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("価格", default=0)
    image = models.CharField("画像", max_length=100)
    context = models.TextField(
        "内容",
    )
    code = models.CharField("商品コード", max_length=50, unique=True)
    created_at = models.DateTimeField("掲載日", auto_now_add=True)

    # リスト用のサムネリサイズ設定
    @property
    def list_thumb_url(self):
        public_id = self.image
        url, _ = cloudinary_url(
            public_id, width=450, height=300, crop="fill", version=int(time.time())
        )
        return url

    # 詳細用のサムネリサイズ設定
    @property
    def detail_thumb_url(self):
        public_id = self.image
        url, _ = cloudinary_url(
            public_id, width=600, height=700, crop="fill", version=int(time.time())
        )
        return url
