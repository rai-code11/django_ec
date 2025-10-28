from django.shortcuts import render
from .models import ProductList
from django.views.generic.list import ListView

# Create your views here.


# dbからidでデータを取ってくる
class ProductListView(ListView):
    model = ProductList
    context_object_name = "product_list"
    template_name = "product_list/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
