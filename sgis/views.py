from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import PacienteForm
from .models import Paciente
from django.contrib import messages 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirecione para a página inicial
            else:
                # Trate o caso em que o usuário não é encontrado
                pass
        else:
            # Trate o caso em que o formulário não é válido
            pass
    else:
        form = AuthenticationForm()
    return render(request, 'sgis/login.html', {'form': form})

def home(request):
    return render(request, 'sgis/home.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PacienteForm

def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('listar_pacientes')
        else:
          print(form.errors)
          messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = PacienteForm()
    return render(request, 'sgis/cadastrar_paciente.html', {'form': form})


def listar_pacientes(request):
        pacientes = Paciente.objects.all()
        return render(request, 'sgis/listar_pacientes.html', {'pacientes': pacientes})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProdutoForm
from .models import Produto

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('listar_produtos')  # Redirecionar para a lista de produtos
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = ProdutoForm()
    return render(request, 'sgis/cadastrar_produto.html', {'form': form})

from django.shortcuts import render
from .models import Produto, EntradaEstoque, Dispensacao

def listar_produtos(request):
    produtos = Produto.objects.all()
    produtos_com_estoque = []
    for produto in produtos:
        # Usa o valor atual do campo estoque do produto
        estoque_disponivel = produto.estoque

        # Adiciona os detalhes de cada entrada de estoque à lista
        detalhes_entradas = []
        entradas = EntradaEstoque.objects.filter(produto=produto)
        for entrada in entradas:
            valor_total = entrada.quantidade * entrada.valor_unitario
            detalhes_entradas.append({
                'lote': entrada.lote,
                'validade': entrada.validade,
                'valor_unitario': entrada.valor_unitario,
                'quantidade': entrada.quantidade,
                'valor_total': valor_total,
            })
        
        produtos_com_estoque.append({
            'produto': produto,
            'estoque_disponivel': estoque_disponivel,
            'detalhes_entradas': detalhes_entradas,
        })
    return render(request, 'sgis/listar_produtos.html', {'produtos_com_estoque': produtos_com_estoque})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FabricanteForm
from .models import Fabricante

def cadastrar_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fabricante cadastrado com sucesso!')
            return redirect('listar_fabricantes')  # Redirecionar para a lista de fabricantes
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = FabricanteForm()
    return render(request, 'sgis/cadastrar_fabricante.html', {'form': form})

def listar_fabricantes(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'sgis/listar_fabricantes.html', {'fabricantes': fabricantes})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FornecedorForm
from .models import Fornecedor

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('listar_fornecedores')  # Redirecionar para a lista de fornecedores
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = FornecedorForm()
    return render(request, 'sgis/cadastrar_fornecedor.html', {'form': form})

def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'sgis/listar_fornecedores.html', {'fornecedores': fornecedores})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Produto
from .forms import EntradaEstoqueForm

def entrada_estoque(request):
    if request.method == 'POST':
        form = EntradaEstoqueForm(request.POST)
        if form.is_valid():
            entrada = form.save(commit=False)
            entrada.valor = entrada.quantidade * entrada.valor_unitario
            entrada.save()

            # Atualiza o estoque do produto
            produto = entrada.produto
            produto.estoque += entrada.quantidade
            produto.save()

            messages.success(request, 'Entrada de estoque registrada com sucesso!')
            return redirect('listar_entradas')  # Redirecionar para a lista de entradas
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = EntradaEstoqueForm()
    return render(request, 'sgis/entrada_estoque.html', {'form': form})

def listar_entradas(request):
    entradas = EntradaEstoque.objects.all()
    return render(request, 'sgis/listar_entradas.html', {'entradas': entradas})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto, Dispensacao
from .forms import DispensacaoForm

import logging
from django.db import transaction

logging.basicConfig(level=logging.DEBUG)

def dispensar_produto(request):
    if request.method == 'POST':
        form = DispensacaoForm(request.POST)
        logging.debug(f"Dados do formulário: {request.POST}")
        if form.is_valid():
            dispensacao = form.save(commit=False)
            produto = dispensacao.produto
            quantidade_dispensada = dispensacao.quantidade

            logging.debug(f"Estoque antes da dispensação: {produto.estoque}")
            logging.debug(f"Quantidade dispensada: {quantidade_dispensada}")

            if quantidade_dispensada <= produto.estoque:
                with transaction.atomic():
                    dispensacao.save()
                    produto.estoque -= quantidade_dispensada
                    produto.save()

                logging.debug(f"Estoque após a dispensação: {produto.estoque}")

                messages.success(request, 'Dispensação registrada com sucesso!')
                return redirect('listar_dispensacoes')
            else:
                messages.error(request, 'Estoque insuficiente para a dispensação.')
        else:
            logging.error(f"Erros no formulário: {form.errors}")
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = DispensacaoForm()
    return render(request, 'sgis/dispensar_produto.html', {'form': form})

def listar_dispensacoes(request):
    dispensacoes = Dispensacao.objects.all()
    return render(request, 'sgis/listar_dispensacoes.html', {'dispensacoes': dispensacoes})

