from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from order.models import Checkout


# プロモコード用のモデル
class PromoCode(models.Model):
    class Meta:
        db_table = "promo_code"

    # チェックアウト1回につき適応できるプロモーションコードは1つにしたいのでOneToOneで1対1の関係にする
    is_used = models.OneToOneField(
        Checkout,
        verbose_name="適応された決済",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="promo_code",
    )
    code = models.CharField(
        "プロモコード",
        max_length=7,
        blank=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z1-9]{7}$",
                message="プロモコードは英数字7桁で入力してください",
            )
        ],
    )
    discount = models.IntegerField(
        "割引額",
        validators=[MinValueValidator(100), MaxValueValidator(1000)],
        default=0,
    )
    # is_used = models.BooleanField("使用済み", default=False)

    # 割引適応後の合計金額を返すメソッド
    def get_discount_amount(self, total_amount):
        # 合計金額がマイナスにならないようにして合計を返す
        return max(total_amount - self.discount, 0)

    # 同じクーポンが2回使用されないようにクーポンがDBに保存されているかを確認する
    def can_use(self):
        return self.is_used is None

    # DBに保存されているかを確認し、保存されていればエラー。保存されていなければ、is_usedフィールドにcheckoutインスタンスを保存して紐付ける
    def mark_used(self, checkout):
        if not self.can_use():
            raise ValueError("このプロモコードは既に使用されています")
        self.is_used = checkout

        # saveだと全てのフィールドを上書き保存してしまうため、特定のフィールドを指定してクエリを軽くする
        self.save(update_fields=["is_used"])
        return self
