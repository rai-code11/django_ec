from django.db import models
from apps.product.models import Product
from cloudinary.utils import cloudinary_url
import time


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    # 下記でカスタムマネージャを呼び出せるようにできるがモデルメソッドで呼び出すことにする
    session_id = models.CharField(max_length=40, unique=True)

    # このCartに紐づいているCartItemを、Product情報も一緒に全部取ってくる
    def get_items(self):
        cart_items = self.cartitem_set.select_related("product").all()
        return cart_items

    # カート内の合計数量を計算するメソッド
    def calculate_total_quantity(self):
        total_quantity = sum(item.quantity for item in self.get_items())
        return total_quantity if total_quantity is not None else 0

    # カートの合計金額を計算するメソッド
    def calculate_total_price(self):
        total_amount = sum(
            item.quantity * item.product.price for item in self.get_items()
        )
        return total_amount if total_amount is not None else 0

    # 各アイテムの小計を計算するメソッド
    def get_item_subtotal(self, cart_item):
        return cart_item.quantity * cart_item.product.price

    # カートアイテムと小計のリストを返す（テンプレート用）
    def get_items_with_subtotals(self):
        return [(item, self.get_item_subtotal(item)) for item in self.get_items()]

    # カートアイテムを消すメソッド
    def clear(self):
        self.delete()


class CartItem(models.Model):
    class Meta:
        db_table = "cart_items"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="uniq_cart_product",
            )
        ]

    cart = models.ForeignKey(Cart, verbose_name="カート", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="商品", on_delete=models.CASCADE)
    quantity = models.IntegerField("個数", default=0)


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
