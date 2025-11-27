from django.urls import path
from .views import List, Create, Update, Delete, CustomerList, CustomerDetails
from basicauth.decorators import basic_auth_required


app_name = "manage"

urlpatterns = [
    path("list/", basic_auth_required(List.as_view()), name="list"),
    path("new/", Create.as_view(), name="create"),
    path("edit/<int:pk>/", Update.as_view(), name="update"),
    path("delete/<int:pk>/", Delete.as_view(), name="delete"),
    path(
        "customer/",
        basic_auth_required(CustomerList.as_view()),
        name="customer_list",
    ),
    path(
        "customer/<int:customer_id>/",
        CustomerDetails.as_view(),
        name="customer_details",
    ),
]
