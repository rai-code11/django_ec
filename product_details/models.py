from django.db import models
from product_list.models import ProductList

# Create your models here.


class ProductDetails(models.Model):
    # 既存データ(ProductList)を引き継ぐ
    product = models.OneToOneField(
        ProductList, on_delete=models.CASCADE, primary_key=True
    )

    # 新しく追加するデータ
    context = models.TextField(
        "内容",
    )
    code = models.CharField("商品コード", max_length=50, unique=True)
    created_at = models.DateTimeField("掲載日", auto_now_add=True)

    class Meta:
        db_table = "product_details"
