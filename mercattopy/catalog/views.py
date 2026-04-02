from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Produto
from django.contrib import messages
from .forms import ProdutoForm


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


def product_create(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect("catalog:product_list")

    else:
        form = ProdutoForm()

    return render(request, "catalog/product_form.html", {"form": form})


def product_update(request, pk):
    product = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("catalog:product_list")

    else:
        form = ProdutoForm(instance=product)

    return render(request, "catalog/product_form.html", {"form": form})


def product_delete(request, pk):
    product = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":

        if product.stock > 0:
            messages.error(request, "Não é possível excluir produto com estoque.")
            return redirect("catalog:product_list")

        product.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect("catalog:product_list")

    return render(request, "catalog/product_confirm_delete.html", {
        "product": product
    })