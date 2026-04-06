from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Produto
from .forms import SaleItemForm
from .models import Sale, SaleItem


SaleItemFormSet = formset_factory(SaleItemForm, extra=3, min_num=1, validate_min=True)

@login_required
@transaction.atomic
def sale_create(request):
    if request.method == "POST":
        formset = SaleItemFormSet(request.POST)

        if formset.is_valid():
            itens = {}
            produtos_ids = []

            for form in formset:
                if not form.cleaned_data:
                    continue

                product = form.cleaned_data["product"]
                quantity = form.cleaned_data["quantity"]

                if product.id not in itens:
                    itens[product.id] = {
                        "product": product,
                        "quantity": 0,
                    }

                itens[product.id]["quantity"] += quantity
                produtos_ids.append(product.id)

            if not itens:
                messages.error(request, "Adicione pelo menos um item à venda.")
                return render(request, "sales/sale_create.html", {"formset": formset})

            produtos_bloqueados = Produto.objects.select_for_update().filter(id__in=itens.keys())

            total = Decimal("0.00")

            for produto in produtos_bloqueados:
                quantidade = itens[produto.id]["quantity"]

                if produto.stock < quantidade:
                    messages.error(
                        request,
                        f"Estoque insuficiente para {produto.name}. "
                        f"Disponível: {produto.stock}, solicitado: {quantidade}."
                    )
                    return render(request, "sales/sale_create.html", {"formset": formset})

            sale = Sale.objects.create(
                total=Decimal("0.00"),
                status="FINALIZADA",
            )

            for produto in produtos_bloqueados:
                quantidade = itens[produto.id]["quantity"]
                unit_price = produto.price
                subtotal = unit_price * quantidade

                SaleItem.objects.create(
                    sale=sale,
                    product=produto,
                    quantity=quantidade,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )

                produto.stock -= quantidade
                produto.save(update_fields=["stock"])

                total += subtotal

            sale.total = total
            sale.save(update_fields=["total"])

            messages.success(request, "Venda registrada com sucesso.")
            return redirect("sales:sale_create")

    else:
        formset = SaleItemFormSet()

    return render(request, "sales/sale_create.html", {"formset": formset})