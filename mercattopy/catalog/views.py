from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Produto
from django.contrib import messages
from .forms import ProdutoForm
from utils.permissions import admin_required

from django.db.models import Sum, Count
from django.utils import timezone
from sales.models import Sale, SaleItem

from ..utils.permissions import admin_required


def is_admin(user):
    return user.groups.filter(name="Admin").exists()


@login_required
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, "catalog/category_list.html", {
        "categories": categorias
    })

@login_required
def lista_produtos(request):
    produtos = Produto.objects.select_related("category").all()
    return render(request, "catalog/product_list.html", {
        "products": produtos
    })

@login_required
def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto.objects.select_related("category"), pk=pk)

    return render(request, "catalog/product_detail.html", {
        "product": produto
    })

@login_required
@admin_required
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

@login_required
@user_passes_test(is_admin)
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

@login_required
@user_passes_test(is_admin)
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

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)


    total_produtos = Produto.objects.count()
    total_categorias = Categoria.objects.count()

    vendas_finalizadas = Sale.objects.filter(status="FINALIZADA")

    total_vendas = vendas_finalizadas.count()

    faturamento_total = vendas_finalizadas.aggregate(
        total=Sum("total")
    )["total"] or 0


    vendas_hoje = vendas_finalizadas.filter(date__date=hoje)

    total_vendas_hoje = vendas_hoje.count()

    faturamento_hoje = vendas_hoje.aggregate(
        total=Sum("total")
    )["total"] or 0


    vendas_mes = vendas_finalizadas.filter(date__date__gte=inicio_mes)

    total_vendas_mes = vendas_mes.count()

    faturamento_mes = vendas_mes.aggregate(
        total=Sum("total")
    )["total"] or 0


    ultimas_vendas = vendas_finalizadas.order_by("-date")[:5]


    top_produtos = (
        SaleItem.objects
        .values("product__name")
        .annotate(total_vendido=Sum("quantity"))
        .order_by("-total_vendido")[:5]
    )


    produtos_estoque_baixo = Produto.objects.filter(stock__lte=3)

    return render(request, "dashboard/dashboard.html", {
        # KPIs gerais
        "total_produtos": total_produtos,
        "total_categorias": total_categorias,
        "total_vendas": total_vendas,
        "faturamento_total": faturamento_total,


        "total_vendas_hoje": total_vendas_hoje,
        "faturamento_hoje": faturamento_hoje,


        "total_vendas_mes": total_vendas_mes,
        "faturamento_mes": faturamento_mes,


        "ultimas_vendas": ultimas_vendas,
        "top_produtos": top_produtos,
        "produtos_estoque_baixo": produtos_estoque_baixo,
    })