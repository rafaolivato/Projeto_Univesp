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

from .models import Produto, EntradaEstoque, SaidaEstoque, Dispensacao
from django.shortcuts import render

from datetime import date, timedelta

def listar_produtos(request):
    produtos_com_estoque = []
    produtos = Produto.objects.all().order_by('descricao')
    hoje = date.today()

    for produto in produtos:
        entradas = EntradaEstoque.objects.filter(itens__produto=produto)
        saidas = SaidaEstoque.objects.filter(produto=produto)
        dispensacoes = Dispensacao.objects.filter(produto=produto)

        total_estoque = 0
        detalhes_entradas = []

        for entrada in entradas:
            itens = entrada.itens.filter(produto=produto)
            for item in itens:
                validade = item.validade
                proximo_vencimento = False

                if validade and validade <= hoje + timedelta(days=60):
                    proximo_vencimento = True

                detalhes_entradas.append({
                    'lote': item.lote,
                    'validade': validade,
                    'valor_unitario': item.valor_unitario,
                    'quantidade': item.quantidade_disponivel,
                    'valor_total': item.quantidade_disponivel * item.valor_unitario,
                    'proximo_vencimento': proximo_vencimento,  # ✅ adiciona esse campo
                })
                total_estoque += item.quantidade_disponivel

        if total_estoque > 0:
            produtos_com_estoque.append({
                'produto': produto,
                'detalhes_entradas': detalhes_entradas,
                'total_estoque': total_estoque,
            })

    return render(request, 'sgis/listar_produtos.html', {'produtos_com_estoque': produtos_com_estoque})



def listar_dispensacoes(request):
    dispensacoes = Dispensacao.objects.all()
    return render(request, 'sgis/listar_dispensacoes.html', {'dispensacoes': dispensacoes})

from django.shortcuts import render

def saiba_mais(request):
    return render(request, 'sgis/saiba_mais.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produto, Dispensacao
from .forms import DispensacaoForm
from .utils import realizar_saida_fifo  # ← certifique-se de importar
from django.db import transaction
import logging

logging.basicConfig(level=logging.DEBUG)

def dispensar_produto(request):
    if request.method == 'POST':
        form = DispensacaoForm(request.POST)
        logging.debug(f"Dados do formulário: {request.POST}")
        if form.is_valid():
            dispensacao = form.save(commit=False)
            produto = dispensacao.produto
            quantidade_dispensada = dispensacao.quantidade

            try:
                with transaction.atomic():
                    valor_total = realizar_saida_fifo(produto, quantidade_dispensada)
                    dispensacao.valor_total = valor_total  # caso deseje salvar isso na model
                    dispensacao.save()

                logging.debug(f"Dispensação realizada com sucesso. Valor total: {valor_total}")
                messages.success(request, 'Dispensação registrada com sucesso!')
                return redirect('listar_produtos')

            except ValueError as e:
                messages.error(request, str(e))

        else:
            logging.error(f"Erros no formulário: {form.errors}")
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = DispensacaoForm()
    return render(request, 'sgis/dispensar_produto.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import SaidaEstoqueForm
from .models import Produto
from .utils import realizar_saida_fifo, retirar_produto_com_validade_mais_proxima
from django.contrib import messages
from django.db import transaction

def saida_estoque(request):
    if request.method == 'POST':
        form = SaidaEstoqueForm(request.POST)
        if form.is_valid():
            saida = form.save(commit=False)
            produto = saida.produto
            quantidade = saida.quantidade
          
            try:
                
                with transaction.atomic():
                   
                    valor_total = realizar_saida_fifo(produto, quantidade)
                    saida.valor_total = valor_total  # certifique-se que existe esse campo se for salvar
                    saida.save()

                messages.success(request, 'Saída de estoque registrada com sucesso.')
                return redirect('saida_estoque')

            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = SaidaEstoqueForm()
    return render(request, 'sgis/saida_estoque.html', {'form': form})

