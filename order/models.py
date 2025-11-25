from django.db import models

# Create your models here.


# 請求情報モデル
class Checkout(models.Model):
    class Meta:
        db_table = "checkout"
        # 登録順に並べる
        ordering = ["-created_at"]

    last_name = models.CharField("姓", max_length=30)
    first_name = models.CharField("名", max_length=30)
    user_name = models.CharField("ユーザー名", max_length=30)
    email = models.EmailField("メールアドレス")
    zip_code = models.CharField("郵便番号", max_length=8)
    prefecture = models.CharField("都道府県", max_length=30)
    city = models.CharField("市区町村", max_length=30)
    street_address = models.CharField("丁目・番地・号", max_length=30)
    building_name = models.CharField("建物名・部屋番号", max_length=30, blank=True)

    total_amount = models.IntegerField("合計金額", default=0)
    total_quantity = models.IntegerField("合計数量", default=0)
    created_at = models.DateTimeField("注文日時", auto_now_add=True, null=True)

    # 完成系の住所を作成する
    @property
    def full_address(self):
        parts = [
            self.prefecture,
            self.city,
            self.street_address,
            self.building_name or "",
        ]
        return " ".join(p for p in parts if p)


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

    # 最後の４桁だけを取得する
    @property
    def last_four_digits(self):
        return self.card_number[-4:]


# 注文商品の明細モデル
class LineItem(models.Model):
    class Meta:
        db_table = "line_item"

    checkout = models.ForeignKey(
        Checkout, verbose_name="注文情報", on_delete=models.CASCADE
    )
    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("価格", default=0)
    quantity = models.IntegerField("数量", default=1)
    subtotal_amount = models.IntegerField("小計", default=0)
