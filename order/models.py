from django.db import models
from checkout.models import CartItem

# Create your models here.


# 請求情報モデル
class Checkout(models.Model):
    class Meta:
        db_table = "checkout"

    last_name = models.CharField("姓", max_length=30)
    first_name = models.CharField("名", max_length=30)
    user_name = models.CharField("ユーザー名", max_length=30)
    email = models.EmailField("メールアドレス")
    zip_code = models.CharField("郵便番号", max_length=8)
    prefecture = models.CharField("都道府県", max_length=30)
    city = models.CharField("市区町村", max_length=30)
    street_address = models.CharField("丁目・番地・号", max_length=30)
    building_name = models.CharField("建物名・部屋番号", max_length=30, blank=True)


# クレジットカード情報モデル
class Payment(models.Model):
    class Meta:
        db_table = "payment"

    checkout = models.ForeignKey(
        Checkout, verbose_name="請求情報", on_delete=models.CASCADE
    )
    card_holder = models.CharField("カード名義人", max_length=50)
    card_number = models.CharField("カード番号", max_length=19)
    expiration_date = models.CharField("有効期限", max_length=10)
    cvv = models.CharField("セキュリティコード", max_length=3)


# 注文商品の明細モデル
class LineItem(models.Model):
    class Meta:
        db_table = "line_item"

    checkout = models.ForeignKey(
        Checkout, verbose_name="注文情報", on_delete=models.CASCADE
    )
    cart_item_name = models.CharField("商品名", max_length=100)
    cart_item_price = models.IntegerField("価格", default=0)
    cart_item_quantity = models.IntegerField("数量", default=1)
