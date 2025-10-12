from django.shortcuts import render
from .models import ProductList

# Create your views here.


# dbからidでデータを取ってくる
def product_list_view(request):
    p_key = ProductList.objects.in_bulk([1, 2, 3, 4, 5, 6, 7, 8])
    return render(request, "product_list/product_list.html", {"p_key": p_key})
