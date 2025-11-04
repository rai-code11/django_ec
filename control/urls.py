from django.urls import path
from .views import List, Create, Update, Delete
from basicauth.decorators import basic_auth_required


app_name = "manage"

urlpatterns = [
    path("list/", basic_auth_required(List.as_view()), name="list"),
    path("new/", Create.as_view(), name="create"),
    path("edit/<int:pk>/", Update.as_view(), name="update"),
    path("delete/<int:pk>/", Delete.as_view(), name="delete"),
]
