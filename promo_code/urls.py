from django.urls import path
from .views import PromoCodeDiscountView


app_name = "promo_code"

urlpatterns = [
    path("apply/", PromoCodeDiscountView.as_view(), name="promo_code"),
]
