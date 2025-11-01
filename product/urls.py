from django.urls import path
from .views import ProductListView, ProductDetailsView


app_name = "product"

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
]
