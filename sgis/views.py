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



from django.shortcuts import render, redirect, get_object_or_404
from .models import Paciente
from django.contrib import messages

def excluir_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        messages.success(request, 'Paciente excluído com sucesso.')
        return redirect('listar_pacientes')  # Redirecione para a página de listagem
    else:
        # Se alguém tentar acessar a URL com GET, redirecione ou exiba um erro
        messages.error(request, 'Método não permitido.')
        return redirect('listar_pacientes')

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
from .models import NotaFiscal, EntradaEstoque, ItemEntradaEstoque
from .forms import NotaFiscalForm, ItemEntradaEstoqueFormSet

def entrada_estoque(request):
    if request.method == 'POST':
        nota_form = NotaFiscalForm(request.POST)
        formset = ItemEntradaEstoqueFormSet(request.POST)

        if nota_form.is_valid() and formset.is_valid():
            nota_fiscal = nota_form.save()
            entrada_estoque = EntradaEstoque.objects.create(nota_fiscal=nota_fiscal)

            itens = formset.save(commit=False)
            for item in itens:
                item.entrada = entrada_estoque
                item.save()

                # Atualiza o estoque
                produto = item.produto
                produto.estoque += item.quantidade
                produto.save()

            return redirect('/listar_entradas')

    else:
        nota_form = NotaFiscalForm()
        formset = ItemEntradaEstoqueFormSet(queryset=ItemEntradaEstoque.objects.none())

    return render(request, 'sgis/entrada_estoque.html', {
        'nota_form': nota_form,
        'formset': formset
    })


def listar_entradas(request):
    entradas = EntradaEstoque.objects.all()
    return render(request, 'sgis/listar_entradas.html', {'entradas': entradas})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto, Dispensacao, EntradaEstoque
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
                return redirect('listar_produtos')  # Redireciona para listar_produtos após a dispensação
            else:
                messages.error(request, 'Estoque insuficiente para a dispensação.')
        else:
            logging.error(f"Erros no formulário: {form.errors}")
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = DispensacaoForm()
    return render(request, 'sgis/dispensar_produto.html', {'form': form})


def listar_produtos(request):
    produtos_com_estoque = []
    produtos = Produto.objects.all()

    for produto in produtos:
        # Filtrando as entradas de estoque relacionadas a este produto
        entradas = EntradaEstoque.objects.filter(itens__produto=produto)
        
        total_estoque = 0  # Inicializa o estoque total para este produto
        detalhes_entradas = []  # A variável precisa ser definida antes de usá-la

        print(f"Produto: {produto.descricao}")  # Para depuração
        print(f"Entradas relacionadas ao produto {produto.descricao}: {entradas.count()} entradas encontradas.")  # Depuração
        
        for entrada in entradas:
            print(f"Entrada de Estoque: {entrada.id}")  # Para depuração
            # Agora vamos acessar os itens (ItemEntradaEstoque) relacionados à entrada
            itens = entrada.itens.filter(produto=produto)

            for item in itens:
                print(f"Item: {item.produto.descricao}, Lote: {item.lote}, Quantidade: {item.quantidade}")  # Depuração
                
                detalhes_entradas.append({
                    'lote': item.lote,  # Acessando 'lote' de ItemEntradaEstoque
                    'validade': item.validade,  # Acessando 'validade' de ItemEntradaEstoque
                    'valor_unitario': item.valor_unitario,  # Acessando 'valor_unitario' de ItemEntradaEstoque
                    'quantidade': item.quantidade,  # Acessando 'quantidade' de ItemEntradaEstoque
                    'valor_total': item.valor_total,  # Acessando 'valor_total' de ItemEntradaEstoque
                })
                
                total_estoque += item.quantidade  # Adiciona a quantidade de cada entrada ao estoque total

        # Verificação de total_estoque antes de adicionar ao contexto
        print(f"Total de estoque para {produto.descricao}: {total_estoque}")  # Depuração

        produtos_com_estoque.append({
            'produto': produto,
            'detalhes_entradas': detalhes_entradas,
            'total_estoque': total_estoque,  # Adiciona o estoque total ao contexto
        })

    return render(request, 'sgis/listar_produtos.html', {'produtos_com_estoque': produtos_com_estoque})


def listar_dispensacoes(request):
    dispensacoes = Dispensacao.objects.all()
    return render(request, 'sgis/listar_dispensacoes.html', {'dispensacoes': dispensacoes})

from django.shortcuts import render

def saiba_mais(request):
    return render(request, 'sgis/saiba_mais.html')

from django.shortcuts import render, redirect
from .forms import SaidaEstoqueForm
from .models import Produto
from django.contrib import messages

def saida_estoque(request):
    if request.method == 'POST':
        form = SaidaEstoqueForm(request.POST)
        if form.is_valid():
            saida = form.save()
            produto = saida.produto
            produto.estoque -= saida.quantidade
            produto.save()
            messages.success(request, 'Saída de estoque registrada com sucesso.')
            return redirect('saida_estoque')
    else:
        form = SaidaEstoqueForm()
    return render(request, 'sgis/saida_estoque.html', {'form': form})