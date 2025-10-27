from django.urls import path
from .views import ProductListView


app_name = "product_list"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
]
