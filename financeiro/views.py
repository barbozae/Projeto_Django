from django.shortcuts import render
from vendas.models import Vendas
from compras.models import Compras
from funcionarios.models import Pagamento
from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When
from datetime import date


def dashboard_vendas(request):
    # Calcular taxas
    def calcular_taxas_vendas(vendas_queryset):
        # Define as regras de taxas por período
        taxas = [
            {
                "inicio": date(2022, 1, 1),
                "fim": date(2022, 8, 1),
                "taxas": {
                    "debito_mastercard": 0.0095,
                    "debito_visa": 0.0095,
                    "debito_elo": 0.0098,
                    "credito_mastercard": 0.0167,
                    "credito_visa": 0.0167,
                    "credito_elo": 0.0167,
                    "hiper": 0.0167,
                    "dinersclub": 0.0167,
                    "american_express": 0.025,
                    "alelo": 0.12,
                    "sodexo": 0.12,
                    "ticket_rest": 0.0714,
                    "vale_refeicao": 0.1274,
                },
            },
            {
                "inicio": date(2022, 8, 2),
                "fim": date(2024, 3, 31),
                "taxas": {
                    "debito_mastercard": 0.0095,
                    "debito_visa": 0.0095,
                    "debito_elo": 0.01,
                    "credito_mastercard": 0.031,
                    "credito_visa": 0.031,
                    "credito_elo": 0.034,
                    "hiper": 0.034,
                    "dinersclub": 0.0167,
                    "american_express": 0.025,
                    "alelo": 0.07,
                    "sodexo": 0.069,
                    "vale_refeicao": 0.069,
                    "ticket_rest": 0.07,
                },
            },
            {
                "inicio": date(2024, 4, 1),
                "fim": date.today(),
                "taxas": {
                    "debito_mastercard": 0.0094,
                    "debito_visa": 0.0094,
                    "debito_elo": 0.0094,
                    "credito_mastercard": 0.0299,
                    "credito_visa": 0.0299,
                    "credito_elo": 0.0299,
                    "hiper": 0.0299,
                    "dinersclub": 0.0299,
                    "american_express": 0.025,
                    "alelo": 0.07,
                    "sodexo": 0.069,
                    "vale_refeicao": 0.069,
                    "ticket_rest": 0.07,
                },
            },
        ]

        # Adiciona condições para cada período
        conditions = []
        for taxa in taxas:
            cond = When(
                data_venda__range=(taxa["inicio"], taxa["fim"]),
                then=sum(F(campo) * valor for campo, valor in taxa["taxas"].items())
            )
            conditions.append(cond)

        # Calcula o total de taxas
        total_taxa = vendas_queryset.aggregate(
            total_taxa=Sum(
                Case(*conditions, output_field=DecimalField(max_digits=10, decimal_places=2))
            )
        )["total_taxa"]

        return total_taxa

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    periodo = request.GET.get('periodo')

    vendas = Vendas.objects.all()
    if data_inicio:
        vendas = vendas.filter(data_venda__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__lte=data_fim)
    if periodo:
        vendas = vendas.filter(periodo=periodo)

    # Agregar valores de vendas
    vendas_total = vendas.aggregate(
        total_rodizio=Sum('rodizio'),
        total_dinheiro=Sum('dinheiro'),
        total_pix=Sum('pix'),
        total_debito=Sum('debito_mastercard') + Sum('debito_visa') + Sum('debito_elo'),
        total_credito=Sum('credito_mastercard') + Sum('credito_visa') + Sum('credito_elo'),
        total_beneficio=Sum('alelo') + Sum('american_express') + Sum('hiper') + Sum('sodexo') + 
                        Sum('ticket_rest') + Sum('vale_refeicao') + Sum('dinersclub'),
        total_socio=Sum('socio')
    )

    total_vendas = (
        (vendas_total['total_dinheiro'] or 0) +
        (vendas_total['total_pix'] or 0) +
        (vendas_total['total_debito'] or 0) +
        (vendas_total['total_credito'] or 0) +
        (vendas_total['total_beneficio'] or 0)
    )

    # Pega o total de rodízios
    total_rodizio = vendas_total['total_rodizio'] or 0 # Garante que será 0 se for None
    # Pegando o total de sóxios
    total_socio = vendas_total['total_socio'] or 0

    if total_vendas and total_rodizio != 0:
        ticket_medio = total_vendas / total_rodizio
    else:
        ticket_medio = 0  # ou algum valor padrão

    # Calcular taxas
    # total_taxas = calcular_taxas_vendas() or 0
    # Calcular taxas com o queryset filtrado
    total_taxas = calcular_taxas_vendas(vendas) or 0

    # Agregar valores de compras
    total_compras = Compras.objects.aggregate(total_despesas=models.Sum('valor_compra'))['total_despesas'] or 0

    # Agregar valores de pagamentos dos funcionários
    total_pagamento_funcionarios = Pagamento.objects.aggregate(
        total_pagamento_funcionarios=models.Sum('valor_pago')
        )['total_pagamento_funcionarios'] or 0

    # Lucro líquido
    lucro_liquido = total_vendas - total_compras - total_pagamento_funcionarios

    # Dados para o contexto do template
    context = {
        'total_dinheiro': vendas_total['total_dinheiro'] or 0,
        'total_pix': vendas_total['total_pix'] or 0,
        'total_debito': vendas_total['total_debito'] or 0,
        'total_credito': vendas_total['total_credito'] or 0,
        'total_beneficio': vendas_total['total_beneficio'] or 0,
        'total_rodizio': total_rodizio,
        'ticket_medio': ticket_medio,
        'total_vendas': total_vendas,
        'vendas_total': vendas_total,
        'total_taxas': total_taxas,
        'total_despesas': total_compras,
        'lucro_liquido': lucro_liquido,
        'pagamento_funcionario': total_pagamento_funcionarios,
        'vendas_por_forma': vendas,
        'total_socio': total_socio,
    }
    return render(request, 'financeiro/dashboard_vendas.html', context)


def dashboard_compras(request):
    ...

def dashboard_funcionarios(request):
    ...

def dashboard_resumo(request):
    ...