from django.shortcuts import render
from vendas.models import Vendas
from compras.models import Compras
from funcionarios.models import Pagamento
from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When
from datetime import date


def dashboard_vendas(request):
    # Calcular taxas
    def calcular_taxas_vendas():
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
                then=Sum(
                    sum(
                        F(campo) * valor
                        for campo, valor in taxa["taxas"].items()
                    )
                ),
            )
            conditions.append(cond)

        # Calcula o total de taxas
        total_taxa = Vendas.objects.aggregate(
            total_taxa=ExpressionWrapper(
                Case(*conditions, output_field=DecimalField(max_digits=10, decimal_places=2)),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )["total_taxa"]

        return total_taxa


    # Agregar valores de vendas
    rodizio = Vendas.objects.aggregate(rodizio=models.Sum('rodizio'))['rodizio'] or 0
    total_dinheiro = Vendas.objects.aggregate(dinheiro=models.Sum('dinheiro'))['dinheiro'] or 0
    total_pix = Vendas.objects.aggregate(pix=models.Sum('pix'))['pix'] or 0

    debito = (
    Vendas.objects.aggregate(
        debito_mastercard=models.Sum('debito_mastercard'),
        debito_visa=models.Sum('debito_visa'),
        debito_elo=models.Sum('debito_elo')
        )
    )
    total_debito = (
        (debito['debito_mastercard'] or 0) +
        (debito['debito_visa'] or 0) +
        (debito['debito_elo'] or 0)
    )

    credito = (
        Vendas.objects.aggregate(
            credito_mastercard=models.Sum('credito_mastercard'),
            credito_visa=models.Sum('credito_visa'),
            credito_elo=models.Sum('credito_elo')
        )
    )
    total_credito = (
        (credito['credito_mastercard'] or 0) +
        (credito['credito_visa'] or 0) +
        (credito['credito_elo'] or 0)
    )

    beneficio = (
        Vendas.objects.aggregate(
            alelo=models.Sum('alelo'),
            american_express=models.Sum('american_express'),
            hiper = models.Sum('hiper'),
            sodexo=models.Sum('sodexo'),
            ticket_rest=models.Sum('ticket_rest'),
            vale_refeicao=models.Sum('vale_refeicao'),
            dinersclub=models.Sum('dinersclub')
        )
    )
    total_beneficio = (
        (beneficio['alelo'] or 0) +
        (beneficio['american_express'] or 0) +
        (beneficio['hiper'] or 0) +
        (beneficio['sodexo'] or 0) +
        (beneficio['ticket_rest'] or 0) +
        (beneficio['vale_refeicao'] or 0) +
        (beneficio['dinersclub'] or 0)
    )

    total_vendas = total_dinheiro + total_pix + total_debito + total_credito + total_beneficio
    ticket_medio = total_vendas / rodizio

    # Calcular taxas
    total_taxas = calcular_taxas_vendas()

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
        'rodizio': rodizio,
        'ticket_medio': ticket_medio,
        'total_vendas': total_vendas,
        'total_taxas': total_taxas,
        'total_despesas': total_compras,
        'lucro_liquido': lucro_liquido,
        'pagamento_funcionario': total_pagamento_funcionarios,
        'receita_por_forma': {
            'dinheiro': total_dinheiro,
            'pix': total_pix,
            'credito': total_credito,
            'debito': total_debito,
            'beneficio': total_beneficio
        },
    }
    return render(request, 'financeiro/dashboard_vendas.html', context)




def dashboard_compras(request):
    ...

def dashboard_funcionarios(request):
    ...

def dashboard_resumo(request):
    ...
    

