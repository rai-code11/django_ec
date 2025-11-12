from django.db import models
from product.models import Product
from cloudinary.utils import cloudinary_url
import time

# Create your models here.


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    session_id = models.CharField(max_length=40, null=True, blank=True, unique=True)


class CartItem(models.Model):
    class Meta:
        db_table = "cart_items"
        models.UniqueConstraint(fields=["cart", "product"], name="uniq_cart_product")

    cart = models.ForeignKey(Cart, verbose_name="カート", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="商品", on_delete=models.CASCADE)
    quantity = models.IntegerField("個数", default=0)
    brief_description = models.CharField("簡易説明", max_length=10)


class Icon(models.Model):
    class Meta:
        db_table = "icon"

    name = models.CharField("名前", max_length=20)
    image = models.CharField("画像", max_length=100)

    # 詳細用のサムネリサイズ設定
    @property
    def icon_thumb_url(self):
        public_id = self.image
        url, _ = cloudinary_url(
            public_id, width=72, height=57, crop="fill", version=int(time.time())
        )
        return url
