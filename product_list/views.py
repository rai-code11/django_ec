from django.shortcuts import render
from .models import ProductList

# Create your views here.


# dbからidでデータを取ってくる
def product_list_view(request):
    product_list = ProductList.objects.all()
    return render(
        request, "product_list/product_list.html", {"product_list": product_list}
    )
