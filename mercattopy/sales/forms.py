from django import forms
from catalog.models import Produto


class SaleItemForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Produto.objects.none(),
        label="Produto"
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantidade"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Produto.objects.filter(is_active=True).order_by("name")