from django.contrib import admin
from .models import Paciente, Produto, Fornecedor, Fabricante, Dispensacao, EntradaEstoque, SaidaEstoque

admin.site.register(Paciente)
admin.site.register(Produto)
admin.site.register(Fornecedor)
admin.site.register(Fabricante)
admin.site.register(Dispensacao)
admin.site.register(EntradaEstoque)
admin.site.register(SaidaEstoque)


