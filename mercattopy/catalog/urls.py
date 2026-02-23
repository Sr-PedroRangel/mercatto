from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("categorias/", views.lista_categorias, name="lista_categorias"),
    path("produtos/", views.lista_produtos, name="lista_produtos"),
    path("produtos/<int:pk>/", views.detalhe_produto, name="detalhe_produto"),
    path("products/create/", views.product_create, name="product_create"),
    path("products/<int:id>/update/", views.product_update, name="product_update"),
    path("products/<int:id>/delete/", views.product_delete, name="product_delete"),
]