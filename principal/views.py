from django.shortcuts import render
from django.http import JsonResponse
from estoque.models import Produto
from vendas.models import Vendas, ProdutosVendas
from estoque.models import Produto
from django.utils import timezone
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .utils import Venda
from django.shortcuts import get_object_or_404
# Create your views here.
def home(request):
    return render(request, 'principal/home.html')

def buscar_produto(request):
    codigo = request.GET.get("codigo")
    try:
        produto = Produto.objects.get(cod_barra=codigo)
        data = {
            "codigo": produto.cod_barra,
            "nome": produto.nome,
            "preco": float(produto.preco),
        }
    except Produto.DoesNotExist:
        data = {"erro": "Produto não encontrado"}
    return JsonResponse(data)

def finalizar_venda(request):
    if request.method == "POST":
        dadosPg={}
        produtos_json = request.POST.get("produtos_json")

        dadosPg['desconto'] = float(request.POST.get("desconto", 0))
        dadosPg['formaPagamento'] = request.POST.get("forma_pagamento")
        dadosPg['valorEntregue'] = float(request.POST.get("valor_entregue", 0))
        dadosPg['troco'] = float(request.POST.get("troco", 0))
        dadosPg['subtotal'] = float(request.POST.get("subtotal", 0))
        dadosPg['total'] = float(request.POST.get("total", 0))
        venda = Venda(dadosPg, json.loads(produtos_json))
        produtos = venda.unirProdutosIguais()
       
        venda.salvarVendas(produtos)

        for i in range(len(produtos)):
            print(produtos[i]['codigo'])
            print(produtos[i]['nome'])
            print(produtos[i]['preco'])
            print(produtos[i]['qtd'])
            print(produtos[i]['subtotal'])

        # Redireciona ou mostra uma mensagem de sucesso
        return redirect("home")  # ou a página que desejar
    return redirect("home")

def juntar_produtos_iguais(produtos):
    """
    Recebe uma lista de produtos e une os produtos iguais somando quantidade e recalculando subtotal.
    Cada produto deve ser um dicionário com as chaves: 'codigo', 'nome', 'preco', 'qtd'

    Retorna uma nova lista de produtos sem duplicatas.
    """
    produtos_unicos = {}

    for produto in produtos:
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

def configuracao(request):
    pass