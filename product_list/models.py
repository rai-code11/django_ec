from django.db import models
from product_list.models import PeoductList

# Create your models here.


class ProductDetails(models.Model):
    # 既存データ(ProductList)を引き継ぐ
    product = models.OneToOneField(
        ProductList, on_delete=models.CASCADE, primary_key=True
    )

    # 新しく追加するデータ
    context = models.TextField()
    code = models.CharField(max_length=50, unique=True)
