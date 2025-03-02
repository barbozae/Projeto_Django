from django.shortcuts import render
from django.views import View
from vendas.models import Vendas
from compras.models import Compras
from funcionarios.models import Pagamento
from django.db.models import Sum, F, DecimalField, Case, When
from decimal import Decimal
from datetime import date


class FiltrosFinanceiro:
    def __init__(self, data_inicio=None, data_fim=None, campo_data='data_venda', 
                 periodo=None, 
                 fornecedor=None, classificacao=None,
                 funcionario = None, tipo_pagamento = None, forma_pagamento = None,
                   **kwargs):
        # Geral
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.campo_data = campo_data  # Define qual campo de data será filtrado (padrão é 'data_compra')
        
        # Vendas
        self.periodo = periodo
        
        # Compras
        self.fornecedor = fornecedor
        self.classificacao = classificacao
        
        # Funcionarios
        self.funcionario = funcionario
        self.tipo_pagamento = tipo_pagamento
        self.forma_pagamento = forma_pagamento

        self.kwargs = kwargs  # Outros filtros adicionais passados como kwargs

    def aplicar_filtros(self, queryset):
        if self.data_inicio:
            queryset = queryset.filter(**{f"{self.campo_data}__gte": self.data_inicio})
        if self.data_fim:
            queryset = queryset.filter(**{f"{self.campo_data}__lte": self.data_fim})

        if self.periodo:  # Aplicando o filtro de período
            queryset = queryset.filter(periodo__in=self.periodo)

        if self.fornecedor:
            # Remove valores vazios da lista de fornecedores
            fornecedores_validos = [f for f in self.fornecedor if f]
            if fornecedores_validos:
                queryset = queryset.filter(fornecedor__id__in=fornecedores_validos)

        if self.classificacao:
            # Remove valores vazios da lista de classificações
            classificacoes_validas = [c for c in self.classificacao if c]
            if classificacoes_validas:
                queryset = queryset.filter(classificacao__in=classificacoes_validas)
        
        if self.funcionario:
            funcionarios_validos = [f for f in self.funcionario if f]
            if funcionarios_validos:
                queryset = queryset.filter(nome_funcionario__id__in=funcionarios_validos)

        if self.tipo_pagamento:
            tipo_pagamentos_validos = [t for t in self.tipo_pagamento if t]
            if tipo_pagamentos_validos:
                queryset = queryset.filter(tipo_pagamento__in=tipo_pagamentos_validos)

        if self.forma_pagamento:
            forma_pagamentos_validos = [f for f in self.forma_pagamento if f]
            if forma_pagamentos_validos:
                queryset = queryset.filter(forma_pagamento__in=forma_pagamentos_validos)
        
        # Adicionando outros filtros passados como kwargs
        for key, value in self.kwargs.items():
            if value:
                queryset = queryset.filter(**{key: value})

        return queryset


class DashboardBaseView(View):
    def calcular_totais_vendas(self, vendas_queryset):
        vendas_total = vendas_queryset.aggregate(
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

        total_rodizio = vendas_total['total_rodizio'] or 0
        total_socio = vendas_total['total_socio'] or 0

        if total_vendas and total_rodizio != 0:
            ticket_medio = total_vendas / total_rodizio
        else:
            ticket_medio = 0

        return {
            'total_dinheiro': vendas_total['total_dinheiro'],
            'total_pix': vendas_total['total_pix'],
            'total_debito': vendas_total['total_debito'],
            'total_credito': vendas_total['total_credito'],
            'total_beneficio': vendas_total['total_beneficio'],
            'total_socio': vendas_total['total_socio'],
            'total_vendas': total_vendas,
            'total_rodizio': total_rodizio,
            'ticket_medio': ticket_medio,
            'vendas_total': vendas_total,
        }

    def calcular_taxas_vendas(self, vendas_queryset):
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

    def calcular_totais_compras(self, compras_queryset):
        total_compras = compras_queryset.aggregate(total_despesas=Sum('valor_compra'))['total_despesas'] or 0
        total_pago = compras_queryset.aggregate(total_despesas=Sum('valor_pago'))['total_despesas'] or 0
        cmv = compras_queryset.filter(classificacao='CMV').aggregate(total_cmv=Sum('valor_compra'))['total_cmv'] or 0
        gasto_fixo = compras_queryset.filter(classificacao='Gasto Fixo').aggregate(total_gasto_fixo=Sum('valor_compra'))['total_gasto_fixo'] or 0
        gasto_variavel = compras_queryset.filter(classificacao='Gasto Variável').aggregate(total_gasto_variavel=Sum('valor_compra'))['total_gasto_variavel'] or 0

        return {
            'total_compras': total_compras,
            'total_pago': total_pago,
            'total_cmv': cmv,
            'total_gasto_fixo': gasto_fixo,
            'total_gasto_variavel': gasto_variavel,
        }

    def calcular_totais_pagamentos(self, pagamentos_queryset):
        total_pagamentos = pagamentos_queryset.aggregate(total_despesas=Sum('valor_pago'))['total_despesas'] or 0
        # rescisao = pagamentos_queryset.filter(tipo_pagamento='Rescisão').aggregate(total_rescisao=Sum('valor_pago'))['total_rescisao'] or 0
        # return {
        #     'total_pagamentos': total_pagamentos,
        #     'total_rescisao': rescisao
        # }
        return total_pagamentos

    def calcular_contas_vencidas(self, compras_queryset):
        # Filtra as compras com data de vencimento menor que a data atual e onde valor_pago é zero ou não existe
        compras_vencidas_nao_pagas = compras_queryset.filter(
            data_vencimento__lt=date.today(),  # Vencidas
            data_pagamento__isnull=True  # Não pagas (data_pagamento é None)
        )

        # Soma o valor total das compras vencidas e não pagas
        total_compras_vencidas = compras_vencidas_nao_pagas.aggregate(
            total_vencidas_nao_pagas=Sum('valor_compra')
        )['total_vencidas_nao_pagas'] or 0

        return total_compras_vencidas
    
    def calcular_contas_dentro_do_prazo(self, compras_queryset):
        # Filtra as compras com data de vencimento maior ou igual à data atual e onde data_pagamento está vazio
        compras_dentro_do_prazo = compras_queryset.filter(
            data_vencimento__gte=date.today(),  # Dentro do prazo (vencimento maior ou igual a hoje)
            data_pagamento__isnull=True  # Não pagas (data_pagamento é None)
        )

        # Soma o valor total das compras não pagas dentro do prazo
        total_compras_dentro_do_prazo = compras_dentro_do_prazo.aggregate(
            total_nao_pagas_dentro_do_prazo=Sum('valor_compra')
        )['total_nao_pagas_dentro_do_prazo'] or 0

        return total_compras_dentro_do_prazo


class DashboardVendasView(DashboardBaseView):    
    def get(self, request):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        periodo = request.GET.get('periodo')

        vendas = Vendas.objects.all()
        filtros = FiltrosFinanceiro(
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            periodo=periodo)
        
        # Aplicar filtros no queryset de vendas
        vendas_filtradas = filtros.aplicar_filtros(vendas)

        totais_vendas = self.calcular_totais_vendas(vendas_filtradas)
        total_taxas = self.calcular_taxas_vendas(vendas_filtradas) or 0

        total_compras = self.calcular_totais_compras(Compras.objects.all())
        total_pagamento_funcionarios = self.calcular_totais_pagamentos(Pagamento.objects.all())

        context = {
            **totais_vendas,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'campo_data': 'data_venda',
            'periodo': periodo,
            'total_taxas': total_taxas,
            'total_despesas': total_compras,
            'pagamento_funcionario': total_pagamento_funcionarios,
            'vendas_por_forma': vendas_filtradas,
        }
        return render(request, 'financeiro/dashboard_vendas.html', context)


class DashboardComprasView(DashboardBaseView):
    def get(self, request):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        classificacao_selecionado = request.GET.getlist('classificacao')
        fornecedores_selecionado = request.GET.getlist('fornecedor')

        compras = Compras.objects.all()
        filtros = FiltrosFinanceiro(
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            campo_data='data_compra',
            classificacao=classificacao_selecionado,
            fornecedor=fornecedores_selecionado)

        # Aplique os filtros na queryset
        compras_filtradas = filtros.aplicar_filtros(compras)

        totais_compras = self.calcular_totais_compras(compras_filtradas)
        fornecedores = Compras.objects.values('fornecedor__id', 'fornecedor__nome_empresa').distinct() #nesse caso estamos pegando o id por ser chave estrangeira
        classificacao = Compras.objects.values('classificacao').distinct()

        context = {
            **totais_compras,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'campo_data': 'data_compra',
            'compras': compras_filtradas,
            'fornecedores_selecionados': fornecedores_selecionado,
            'fornecedores': fornecedores,
            'classificacao_selecionado': classificacao_selecionado,
            'classificacao': classificacao,
        }
        return render(request, 'financeiro/dashboard_compras.html', context)


class DashboardFuncionariosView(DashboardBaseView):
    def get(self, request):
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        funcionario_selecionado = request.GET.getlist('nome_funcionario')
        tipo_pagamento_selecionado = request.GET.getlist('tipo_pagamento')
        forma_pagamento_selecionado = request.GET.getlist('forma_pagamento')

        funcionarios = Pagamento.objects.all()

        filtros = FiltrosFinanceiro(
            data_inicio=data_inicio,
            data_fim=data_fim,
            campo_data='data_pagamento',
            funcionario=funcionario_selecionado,
            tipo_pagamento=tipo_pagamento_selecionado,
            forma_pagamento=forma_pagamento_selecionado
            )
        
        # Aplicar filtros no queryset de funcionários
        funcionarios_filtrado = filtros.aplicar_filtros(funcionarios)
        tipo_pagamentos_agrupados = funcionarios_filtrado.values('tipo_pagamento').annotate(total_valor_pago=Sum('valor_pago'))
        forma_pagamentos_agrupados = funcionarios_filtrado.values('forma_pagamento').annotate(total_valor_pago=Sum('valor_pago'))
        
        # Totais de pagamentos
        total_pagamentos = self.calcular_totais_pagamentos(funcionarios_filtrado)
        total_tipo_pagamento = sum(item['total_valor_pago'] for item in tipo_pagamentos_agrupados)
        total_forma_pagamento = sum(item['total_valor_pago'] for item in forma_pagamentos_agrupados)

        # Dados para o filtro
        nome_funcionario = Pagamento.objects.values('nome_funcionario__id', 'nome_funcionario__nome_funcionario').distinct()
        tipos_pagamento = Pagamento.objects.values('tipo_pagamento').distinct()
        formas_pagamento = Pagamento.objects.values('forma_pagamento').distinct()

        # Agrupar pagamentos por tipo de pagamento e funcionário
        funcionarios_por_tipo = (
            funcionarios_filtrado.values('tipo_pagamento', 'nome_funcionario__nome_funcionario')
            .annotate(total_valor_pago=Sum('valor_pago'))
            .order_by('tipo_pagamento', 'nome_funcionario__nome_funcionario')
        )

        # Agrupar pagamentos por forma pagamento e funcionário
        funcionarios_por_forma = (
            funcionarios_filtrado.values('forma_pagamento', 'nome_funcionario__nome_funcionario')
            .annotate(total_valor_pago=Sum('valor_pago'))
            .order_by('forma_pagamento', 'nome_funcionario__nome_funcionario')
        )

        # Agregar valores pagos por cargo
        pagamentos_por_cargo = (
            Pagamento.objects.select_related('nome_funcionario')
            .values('nome_funcionario__contratacao__cargo')
            .annotate(total_valor_pago=Sum('valor_pago'))
            .order_by('nome_funcionario__contratacao__cargo')
        )

        # Listar funcionários e seus valores pagos, agrupados por cargo
        funcionarios_por_cargo = (
            Pagamento.objects.select_related('nome_funcionario')
            .values(
                'nome_funcionario__contratacao__cargo',
                'nome_funcionario__nome_funcionario',
                'valor_pago'
            )
            .order_by('nome_funcionario__contratacao__cargo')
        )

        # Agregar valores pagos por setor
        pagamentos_por_setor = (
            Pagamento.objects.select_related('nome_funcionario')
            .values('nome_funcionario__contratacao__setor')
            .annotate(total_valor_pago=Sum('valor_pago'))
            .order_by('nome_funcionario__contratacao__setor')
        )

        funcionario_por_setor = (
            Pagamento.objects.select_related('nome_funcionario')
            .values(
                'nome_funcionario__contratacao__setor',
                'nome_funcionario__nome_funcionario',
                'valor_pago'
            )
            .order_by('nome_funcionario__contratacao__setor')
        )

        context = {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'campo_data': 'data_pagamento',
            'funcionarios': funcionarios_filtrado,
            'nome_funcionarios': nome_funcionario,
            'funcionario_selecionados': funcionario_selecionado,
            'tipo_pagamento_selecionado': tipo_pagamento_selecionado,
            'forma_pagamento_selecionado': forma_pagamento_selecionado,
            'total_pagamentos': total_pagamentos,
            'tipos_pagamento': tipos_pagamento,
            'formas_pagamento': formas_pagamento,
            'tipo_pagamentos_agrupados': tipo_pagamentos_agrupados,
            'forma_pagamentos_agrupados': forma_pagamentos_agrupados,
            'total_tipo_pagamento': total_tipo_pagamento,
            'total_forma_pagamento': total_forma_pagamento,
            'funcionarios_por_tipo': funcionarios_por_tipo,
            'funcionarios_por_forma': funcionarios_por_forma,
            'pagamentos_por_cargo': pagamentos_por_cargo,
            'funcionarios_por_cargo': funcionarios_por_cargo,
            'pagamentos_por_setor': pagamentos_por_setor,
            'funcionario_por_setor': funcionario_por_setor,
        }
        return render(request, 'financeiro/dashboard_funcionarios.html', context)


class DashboardResumoView(DashboardBaseView):
    def get(self, request):
        # Filtros e dados de vendas
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        vendas = Vendas.objects.all()
        filtros_vendas = FiltrosFinanceiro(
            data_inicio=data_inicio, 
            data_fim=data_fim, 
        )
        vendas_filtradas = filtros_vendas.aplicar_filtros(vendas)
        totais_vendas = self.calcular_totais_vendas(vendas_filtradas)
        fundo_caixa = totais_vendas['total_vendas'] * Decimal('0.06') or Decimal('0')
        total_taxas_vendas = self.calcular_taxas_vendas(vendas_filtradas) or 0

        # Filtros e dados de compras
        classificacao_selecionada = request.GET.getlist('classificacao_compras')
        fornecedores_selecionados = request.GET.getlist('fornecedor_compras')

        compras = Compras.objects.all()
        filtros_compras = FiltrosFinanceiro(
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            campo_data='data_compra',
            classificacao=classificacao_selecionada,
            fornecedor=fornecedores_selecionados,
        )
        compras_filtradas = filtros_compras.aplicar_filtros(compras)
        totais_compras = self.calcular_totais_compras(compras_filtradas)
        total_compras_vencidas = self.calcular_contas_vencidas(compras_filtradas)
        # Calcular o total das contas não pagas dentro do prazo
        total_compras_dentro_do_prazo = self.calcular_contas_dentro_do_prazo(compras_filtradas)

        # Filtros e dados de pagamentos de funcionários
        data_inicio_funcionarios = request.GET.get('data_inicio_funcionarios')
        data_fim_funcionarios = request.GET.get('data_fim_funcionarios')
        funcionario_selecionado = request.GET.getlist('nome_funcionario')
        tipo_pagamento_selecionado = request.GET.getlist('tipo_pagamento')
        forma_pagamento_selecionado = request.GET.getlist('forma_pagamento')

        funcionarios = Pagamento.objects.all()
        filtros_funcionarios = FiltrosFinanceiro(
            data_inicio=data_inicio,
            data_fim=data_fim,
            campo_data='data_pagamento',
            funcionario=funcionario_selecionado,
            tipo_pagamento=tipo_pagamento_selecionado,
            forma_pagamento=forma_pagamento_selecionado,
        )

        funcionarios_filtrados = filtros_funcionarios.aplicar_filtros(funcionarios)
        total_pagamentos_funcionarios = self.calcular_totais_pagamentos(funcionarios_filtrados)
        # total_compras_dentro_do_prazo = self.calcular_contas_dentro_do_prazo(compras_filtradas)

        total_rescisao = (
        funcionarios_filtrados.filter(tipo_pagamento='Rescisão')
        .aggregate(total=Sum('valor_pago'))['total'] or 0
    )

        # Cálculo do lucro líquido
        lucro_liquido = totais_vendas['total_vendas'] - totais_compras['total_compras'] - total_pagamentos_funcionarios

        # Contexto para o template
        context = {
            # Dados de filtro
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            # Dados de vendas
            'totais_vendas': totais_vendas['total_vendas'],
            'lucro_liquido': lucro_liquido,
            'fundo_caixa': fundo_caixa,
            # 'total_taxas_vendas': total_taxas_vendas,
            # 'data_inicio_vendas': data_inicio_vendas,
            # 'data_fim_vendas': data_fim_vendas,

            # Dados de compras
            'totais_compras': totais_compras['total_compras'],
            'total_pago_compras': totais_compras['total_pago'],
            # 'data_inicio_compras': data_inicio_compras,
            # 'data_fim_compras': data_fim_compras,
            'cmv': totais_compras['total_cmv'],
            'gasto_fixo': totais_compras['total_gasto_fixo'],
            'gasto_variavel': totais_compras['total_gasto_variavel'],
            'total_compras_vencidas': total_compras_vencidas,
            'total_compras_dentro_do_prazo': total_compras_dentro_do_prazo,
            # 'classificacao_selecionada': classificacao_selecionada,
            # 'fornecedores_selecionados': fornecedores_selecionados,

            # Dados de pagamentos de funcionários
            'total_pagamentos_funcionarios': total_pagamentos_funcionarios,
            'data_inicio_funcionarios': data_inicio_funcionarios,
            'data_fim_funcionarios': data_fim_funcionarios,
            'funcionario_selecionado': funcionario_selecionado,
            'tipo_pagamento_selecionado': tipo_pagamento_selecionado,
            'forma_pagamento_selecionado': forma_pagamento_selecionado,
            'total_rescisao': total_rescisao,

            # Lucro líquido
            'lucro_liquido': lucro_liquido,
        }

        return render(request, 'financeiro/dashboard_resumo.html', context)