from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["name", "description", "price", "stock", "is_active", "category"]


    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError("O preço não pode ser negativo.")

        return price


    def clean_stock(self):
        stock = self.cleaned_data.get("stock")

        if stock is not None and stock < 0:
            raise forms.ValidationError("O estoque não pode ser negativo.")

        return stock


    def clean_name(self):
        name = self.cleaned_data.get("name")

        if len(name) < 3:
            raise forms.ValidationError("Nome deve ter pelo menos 3 caracteres.")

        return name


    def clean_category(self):
        category = self.cleaned_data.get("category")

        if not category.is_active:
            raise forms.ValidationError("Não é possível usar categoria inativa.")

        return category