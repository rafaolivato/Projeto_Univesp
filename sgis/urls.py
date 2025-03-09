from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('cadastrar_paciente/', views.cadastrar_paciente, name='cadastrar_paciente'),
    path('listar_pacientes/', views.listar_pacientes, name='listar_pacientes'),
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('cadastrar_fabricante/', views.cadastrar_fabricante, name='cadastrar_fabricante'),
    path('listar_fabricantes/', views.listar_fabricantes, name='listar_fabricantes'),
    path('entrada_estoque/', views.entrada_estoque, name='entrada_estoque'),
    path('listar_entradas/', views.listar_entradas, name='listar_entradas'),
    path('cadastrar_fornecedor/', views.cadastrar_fornecedor, name='cadastrar_fornecedor'),
    path('listar_fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('dispensar_produto/', views.dispensar_produto, name='dispensar_produto'),
    path('listar_dispensacoes/', views.listar_dispensacoes, name='listar_dispensacoes'),
]
