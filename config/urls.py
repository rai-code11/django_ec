from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", TemplateView.as_view(template_name="hello.html")),
    path(
        "products/",
        include("apps.product.urls"),
    ),
    path("", TemplateView.as_view(template_name="product/list.html")),
    path(
        "manage/products/",
        include("apps.manage.urls"),
    ),
    path("cart/", include("apps.cart.urls")),
    path("order/", include("apps.order.urls")),
    path("promo/", include("apps.promo_code.urls")),
]
