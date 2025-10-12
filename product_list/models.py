from django.db import models

# Create your models here.


class ProductList(models.Model):
    class Meta:
        db_table = "product_list"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images/")
