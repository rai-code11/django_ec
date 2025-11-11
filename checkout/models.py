from django.db import models
from product.models import Product

# Create your models here.


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    session_id = models.CharField(max_length=40, null=True, blank=True, unique=True)


class CartItem(models.Model):
    class Meta:
        db_table = "cart_items"
        models.UniqueConstraint(fields=["cart", "product"], name="uniq_cart_product")

    cart = models.ForeignKey(Cart, verbose_name="カート")
    product = models.ForeignKey(Product, verbose_name="商品")
    quantity = models.IntegerField("個数", default=0)
    brief_description = models.CharField("簡易説明", max_length=10)
