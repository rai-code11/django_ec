from django.urls import path
from .views import product_list_view


app_name = "product_list"

urlpatterns = [
    path("", product_list_view, name="product_list"),
]
