from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

# Create your models here.


class ProductList(models.Model):
    class Meta:
        db_table = "product_list"

    id = models.AutoField("id", primary_key=True)
    name = models.CharField("商品名", max_length=100)
    price = models.IntegerField("価格", default=0)
    image = models.ImageField("元の画像", upload_to="images/")

    productlist_img = ImageSpecField(
        source="image",
        processors=[ResizeToFill(450, 300)],
        format="JPEG",
        options={"quality": 85},
    )

    productdetails_img = ImageSpecField(
        source="image",
        processors=[ResizeToFit(600, 700)],
        format="JPEG",
        options={"quality": 90},
    )

    def __str__(self):
        return self.name
