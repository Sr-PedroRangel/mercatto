from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("categorias/", views.lista_categorias, name="lista_categorias"),
    path("produtos/", views.lista_produtos, name="lista_produtos"),
    path("produtos/<int:pk>/", views.detalhe_produto, name="detalhe_produto"),
]