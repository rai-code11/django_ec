from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from product.models import Product
from django.urls import reverse_lazy

# Create your views here.


class List(ListView):
    model = Product
    context_object_name = "list"
    template_name = "control/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Create(CreateView):
    model = Product
    fields = "__all__"
    template_name = "control/form.html"

    success_url = "/manage/products/list/"


class Update(UpdateView):
    model = Product
    fields = "__all__"
    template_name = "control/form.html"

    success_url = "/manage/products/list/"


class Delete(DeleteView):
    model = Product
    template_name = "control/delete.html"

    success_url = reverse_lazy("manage:list")
