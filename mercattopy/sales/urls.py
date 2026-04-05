from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    path("nova/", views.sale_create, name="sale_create"),
]