from django.db import models
from localflavor.br.models import BRCPFField


class Endereco(models.Model):
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=20, verbose_name="Número")
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

class Paciente(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome Completo")
    cnes = models.CharField(max_length=15, blank=True, null=True)
    cpf = BRCPFField(unique=True)
    data_nascimento = models.DateField()
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nome

class Fabricante(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    apresentacao = models.CharField(max_length=50, verbose_name="Apresentação")
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE)
    estoque = models.IntegerField(default=0)  # Adicionado o campo estoque
       

    def __str__(self):
        return self.descricao

class Estoque(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='estoques')
    quantidade = models.IntegerField()
    ultima_atualizacao = models.DateTimeField(auto_now_add=True)

from django.db import models

class Dispensacao(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, blank=True, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidades"

class Fornecedor(models.Model):
    nome = models.CharField(max_length=250)
    cnpj = models.CharField(max_length=14)
    endereco = models.CharField(max_length=250, verbose_name="Endereço")
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
class NotaFiscal(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    data_nota = models.DateField(verbose_name="Data da Nota Fiscal")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Total", default=0.00)
    numero_nota_fiscal = models.CharField(max_length=20, verbose_name="Número da Nota Fiscal", default=000)

    

    def __str__(self):
        return f"Nota Fiscal {self.numero_nota_fiscal} - {self.fornecedor.nome}"

import datetime
from django.utils import timezone


class EntradaEstoque(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE)  # Apenas uma vez
    data_entrada = models.DateField(default=timezone.now)
    

    def __str__(self):
        return f"Entrada {self.id} - {self.nota_fiscal}"
      
    
class ItemEntradaEstoque(models.Model):
    entrada = models.ForeignKey(EntradaEstoque, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    lote = models.CharField(max_length=100) 
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    validade = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade}"

    @property
    def valor_total(self):
        return self.quantidade * self.valor_unitario


from django.db import models

class SaidaEstoque(models.Model):
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    motivo = models.TextField()
    data_saida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.produto.descricao} - {self.quantidade}'