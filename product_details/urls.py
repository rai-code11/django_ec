from django.urls import path
from .views import ProductDetailsView


app_name = "product_details"

urlpatterns = [
    path("<int:pk>/", ProductDetailsView.as_view(), name="product_details"),
]
