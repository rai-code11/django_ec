from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from order.models import Checkout


# プロモコード用のモデル
class PromoCode(models.Model):
    class Meta:
        db_table = "promo_code"

    # チェックアウト1回につき適応できるプロモーションコードは1つにしたいのでOneToOneで1対1の関係にする
    used_checkout = models.OneToOneField(
        Checkout,
        verbose_name="適応された決済",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="promo_code",
    )
    promo_code = models.CharField(
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
    is_used = models.BooleanField("使用済み", default=False)

    # 割引適応後の合計金額を返すメソッド
    def get_discount_amount(self, total_amount):
        # 合計金額がマイナスにならないようにして合計を返す
        return max(total_amount - self.discount, 0)

    # 同じクーポンが2回使用されないように割引適応後にクーポンの使用マークを変更するメソッド
    def mark_used(self):
        self.is_used = True
        # saveだと全てのフィールドを上書き保存してしまうため、特定のフィールドを指定してクエリを軽くする
        self.save(update_fields=["is_used"])
