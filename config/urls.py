from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", TemplateView.as_view(template_name="hello.html")),
    path(
        "products/",
        include("product.urls"),
    ),
    path("", TemplateView.as_view(template_name="product/list.html")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
