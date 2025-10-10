from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class ProductList(TemplateView):
    template_name = "product_list/product_list.html"


product_list = ProductList.as_view()
