from django.db import models


# プロモコード用のモデル
class Promo(models.Model):
    class Meta:
        db_table = "promo_code"

    promo_code = models.CharField(max_length=7, blank=True, unique=True)
