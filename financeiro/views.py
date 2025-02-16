from django.shortcuts import render
from vendas.models import Vendas
from compras.models import Compras
from django.db import models


def dashboard_vendas(request):
    # Agregar valores de vendas
    total_vendas = Vendas.objects.aggregate(total_receita=models.Sum('dinheiro'))['total_receita'] or 0
    total_pix = Vendas.objects.aggregate(total_pix=models.Sum('pix'))['total_pix'] or 0
    total_credito = Vendas.objects.aggregate(total_credito=models.Sum('credito_mastercard'))['total_credito'] or 0
    total_debito = Vendas.objects.aggregate(total_debito=models.Sum('debito_mastercard'))['total_debito'] or 0

    # Agregar valores de compras
    total_compras = Compras.objects.aggregate(total_despesas=models.Sum('valor_compra'))['total_despesas'] or 0

    # Lucro líquido
    lucro_liquido = total_vendas - total_compras

    # Dados para o contexto do template
    context = {
        'total_receita': total_vendas,
        'total_despesas': total_compras,
        'lucro_liquido': lucro_liquido,
        'receita_por_forma': {
            'dinheiro': total_vendas,
            'pix': total_pix,
            'credito': total_credito,
            'debito': total_debito,
        },
    }
    return render(request, 'financeiro/dashboard_vendas.html', context)

