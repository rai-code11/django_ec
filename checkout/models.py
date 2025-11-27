from django.db import models
from product.models import Product
from cloudinary.utils import cloudinary_url
from django.db.models import Sum
import time

# Create your models here.


# カスタムマネージャの設定
# カートを消す処理を定義
# class CartManager(models.Manager):
#     def clear_by_session(self, session_key):
#         # filter()を使って該当するクエリセットを取得
#         queryset = self.filter(session_id=session_key)

#         # クエリセットに対して直接delete()を呼び出す
#         # データベースで直接DELETEクエリが実行される
#         deleted_count, _ = queryset.delete()

#         # 削除されたレコード数が0より大きければ成功と見なす
#         return deleted_count > 0


class Cart(models.Model):
    class Meta:
        db_table = "cart"

    # 下記でカスタムマネージャを呼び出せるようにできるがモデルメソッドで呼び出すことにする
    # objects = CartManager()
    session_id = models.CharField(max_length=40, null=True, blank=True, unique=True)

    # このCartに紐づいているCartItemを、Product情報も一緒に全部取ってくる
    def get_items(self):
        n_1 = self.cartitem_set.select_related("product").all()
        return n_1

    # カート内の合計数量を計算するメソッド
    def calculate_total_quantity(self):
        # cart_items = CartItem.objects.filter(cart=self)
        # total_quantity = sum(item.quantity for item in cart_items)

        # 取り出さずにDB側で合計を計算できるので高速になる
        total_quantity = sum(item.quantity for item in self.get_items())
        # if total_quantity is None:
        #     total_quantity = 0

        # return total_quantity

        return total_quantity if total_quantity is not None else 0

    # カートの合計金額を計算するメソッド
    def calculate_total_price(self):
        total_amount = sum(
            item.quantity * item.product.price for item in self.get_items()
        )
        return total_amount if total_amount is not None else 0

    # カートアイテムを消すメソッド
    def clear(self):
        self.delete()


class CartItem(models.Model):
    class Meta:
        db_table = "cart_items"
        models.UniqueConstraint(fields=["cart", "product"], name="uniq_cart_product")

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
