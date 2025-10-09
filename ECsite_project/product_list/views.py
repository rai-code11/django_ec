from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "product_list/product_list.html"


product_list = IndexView.as_view()
