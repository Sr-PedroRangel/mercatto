from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("categorias/", views.lista_categorias, name="category_list"),

    path("produtos/", views.lista_produtos, name="product_list"),

    path("produtos/<int:pk>/", views.detalhe_produto, name="product_detail"),

    path("produtos/criar/", views.product_create, name="product_create"),

    path("produtos/<int:pk>/editar/", views.product_update, name="product_update"),

    path("produtos/<int:pk>/excluir/", views.product_delete, name="product_delete"),
]