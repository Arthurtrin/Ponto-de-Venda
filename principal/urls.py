from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("buscar-produto/", views.buscar_produto, name="buscar_produto"),
    path("configuracoes/", views.configuracao, name="configuracao"),
    path("finalizar-venda/", views.finalizar_venda, name="finalizar_venda"),
]