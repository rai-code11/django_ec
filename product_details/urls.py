from django.urls import path
from .views import product_details_view


app_name = "product_details"

urlpatterns = [
    path("", product_details_view, name="product_details"),
]
