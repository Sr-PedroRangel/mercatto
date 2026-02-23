from django.shortcuts import render, get_object_or_404
from .models import Categoria, Produto



def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "catalog/category_list.html", {
        "categories": categorias
    })



def lista_produtos(request):
    produtos = Produto.objects.select_related("category").all()
    return render(request, "catalog/product_list.html", {
        "products": produtos
    })



def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto.objects.select_related("category"), pk=pk)

    return render(request, "catalog/product_detail.html", {
        "product": produto
    })