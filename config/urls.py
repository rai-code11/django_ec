from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", TemplateView.as_view(template_name="hello.html")),
    path(
        "products/",
        include("product.urls"),
    ),
    path("", TemplateView.as_view(template_name="product/list.html")),
    path(
        "manage/products/",
        include("control.urls"),
    ),
    path("checkout/", include("checkout.urls")),
    path("order/", include("order.urls")),
]
