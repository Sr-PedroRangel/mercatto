from django.db import models


class Categoria(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField("Ativo?", default=True)

    def __str__(self):
        return self.name


class Produto(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField("Ativo?", default=True)

    category = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="products"
    )


    def __str__(self):
        return self.name