from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", TemplateView.as_view(template_name="hello.html")),
    path(
        "product_list/",
        include("product_list.urls"),
        name="product_list",
    ),
    path("", TemplateView.as_view(template_name="product_list/product_list.html")),
]
