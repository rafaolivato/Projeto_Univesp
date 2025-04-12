from decimal import Decimal
from .models import ItemEntradaEstoque

def realizar_saida_fifo(produto, quantidade_a_retirar):
    # Ajuste aqui para usar data_entrada no lugar de data
    itens = ItemEntradaEstoque.objects.filter(produto=produto, quantidade_disponivel__gt=0).order_by('entrada__data_entrada')
    
    quantidade_restante = quantidade_a_retirar
    valor_total = Decimal('0.00')

    for item in itens:
        if quantidade_restante == 0:
            break

        quantidade_usada = min(item.quantidade_disponivel, quantidade_restante)
        valor_total += quantidade_usada * item.valor_unitario

        # Atualiza o item
        item.quantidade_disponivel -= quantidade_usada
        item.save()

        quantidade_restante -= quantidade_usada

    if quantidade_restante > 0:
        raise ValueError("Estoque insuficiente para o produto: {}".format(produto))

    return valor_total


from .models import ItemEntradaEstoque
from django.utils import timezone

def retirar_produto_com_validade_mais_proxima(produto, quantidade_necessaria):
    """
    Retira produtos com base na validade mais próxima (FIFO), atualizando a quantidade_disponivel.
    Retorna os lotes utilizados com suas quantidades.
    """
    itens = ItemEntradaEstoque.objects.filter(
        produto=produto,
        quantidade_disponivel__gt=0,
        validade__gte=timezone.now().date()
    ).order_by('validade')

    lotes_utilizados = []
    quantidade_restante = quantidade_necessaria

    for item in itens:
        if quantidade_restante <= 0:
            break

        retirar = min(item.quantidade_disponivel, quantidade_restante)
        item.quantidade_disponivel -= retirar
        item.save()

        lotes_utilizados.append({
            'item': item,
            'quantidade': retirar,
            'valor_unitario': item.valor_unitario,
        })

        quantidade_restante -= retirar

    if quantidade_restante > 0:
        raise ValueError("Estoque insuficiente para este produto.")

    return lotes_utilizados
