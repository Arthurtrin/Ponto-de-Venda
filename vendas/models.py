from django.db import models
from estoque.models import Produto

# Create your models here.
class Vendas(models.Model):
    cliente = models.CharField(max_length=30, default='BALCÃO')
    formaPagamento = models.CharField(max_length=30)
    total = models.FloatField()
    descontoDinheiro = models.FloatField(default=0)
    descontoPorcento = models.FloatField(default=0)
    acrescimo = models.FloatField(default=0)
    valorEntregue = models.FloatField()
    troco = models.FloatField(default=0)
    dataHora = models.DateTimeField()

    def __str__(self):
        return f"{self.nome} - {self.dataHora}"

class ProdutosVendas(models.Model):
    venda = models.ForeignKey(Vendas, on_delete=models.PROTECT)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    preco = models.FloatField()
    quantidade = models.IntegerField()
    subtotal = models.FloatField()

    def __str__(self):
        return f"{self.venda} - {self.codProduto}"
