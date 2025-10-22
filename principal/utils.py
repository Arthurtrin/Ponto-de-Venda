from vendas.models import Vendas, ProdutosVendas
from estoque.models import Produto
from django.utils import timezone
from django.shortcuts import get_object_or_404

class Venda:
    def __init__(self, dadosPg, produtos):
        self.desconto = dadosPg['desconto']  
        self.valorEntregue = dadosPg['valorEntregue']
        self.troco = dadosPg['troco']
        self.subtotal = dadosPg['subtotal']
        self.total = dadosPg['total']
        self.formaPagamento = self.formataPagamento(dadosPg['formaPagamento'])
        self.produtos = produtos

    def formataPagamento(self, formaPagamento):
        formaPagamento = formaPagamento.replace("_", " ") # -> "cartao pix"
        formaPagamento = formaPagamento.title() # -> "Cartao Pix"
        formaPagamento = formaPagamento.replace(" ", " + ", 1) # -> "Cartao + Pix"
        return formaPagamento
    
    def salvarVendas(self, produtos):
        venda = Vendas.objects.create(
            cliente="BALCÃO",
            formaPagamento= self.formaPagamento,
            total=self.total,
            troco=self.troco,
            descontoDinheiro = 0,
            descontoPorcento = 0,
            acrescimo = 0,
            valorEntregue=self.valorEntregue,
            dataHora=timezone.now()
        )
        
        for i in range(len(produtos)):
            produto = get_object_or_404(Produto, cod_barra=produtos[i]['codigo']) 
            ProdutosVendas.objects.create(
                venda = venda,
                produto = produto,
                preco = produtos[i]['preco'],
                quantidade = produtos[i]['qtd'],
                subtotal = produtos[i]['subtotal']
            )

    def unirProdutosIguais(self):
        """
        Recebe uma lista de produtos e une os produtos iguais somando quantidade e recalculando subtotal.
        Cada produto deve ser um dicionário com as chaves: 'codigo', 'nome', 'preco', 'qtd'

        Retorna uma nova lista de produtos sem duplicatas.
        """
        produtos_unicos = {}

        for produto in self.produtos:
            codigo = produto['codigo']
            if codigo in produtos_unicos:
                # Produto já existe, soma a quantidade
                produtos_unicos[codigo]['qtd'] += produto['qtd']
                # Recalcula o subtotal
                produtos_unicos[codigo]['subtotal'] = produtos_unicos[codigo]['qtd'] * produtos_unicos[codigo]['preco']
            else:
                # Adiciona produto pela primeira vez
                produtos_unicos[codigo] = {
                    'codigo': produto['codigo'],
                    'nome': produto['nome'],
                    'preco': produto['preco'],
                    'qtd': produto['qtd'],
                    'subtotal': produto['preco'] * produto['qtd']
                }

        # Retorna a lista de produtos unificados
        return list(produtos_unicos.values())
    

        
        


    
        