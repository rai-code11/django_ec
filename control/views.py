from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from product.models import Product
from order.models import LineItem
from django.urls import reverse_lazy

# Create your views here.


class List(ListView):
    model = Product
    context_object_name = "list"
    template_name = "control/list.html"


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


class ParticipantList(ListView):
    model = LineItem
    context_object_name = "participant"
    template_name = "control/participant_list.html"
