from django.urls import path
from .views import CartDetailView, AddToCartView, RemoveFromCartView


app_name = "checkout"

urlpatterns = [
    path("", CartDetailView.as_view(), name="checkout"),
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path(
        "remove/<int:product_id>",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
]
