from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'principal/home.html')

from django.http import JsonResponse
from estoque.models import Produto  # supondo que tenha um model Produto

def buscar_produto(request):
    codigo = request.GET.get("codigo")
    try:
        produto = Produto.objects.get(cod_barra=codigo)
        data = {
            "codigo": produto.cod_barra,
            "nome": produto.nome,
            "preco": float(produto.preco),  # converter para número
        }
    except Produto.DoesNotExist:
        data = {"erro": "Produto não encontrado"}
    return JsonResponse(data)