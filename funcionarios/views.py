from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Cadastro, Contratacao, Pagamento, Rescisao
from project.mixins import TenantQuerysetMixin, HandleNoPermissionMixin
from project.utils import generate_success_url


class CadastroListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_list.html'  # Garante que o template correto será usado
    context_object_name = 'funcionarios_list'
    permission_required = 'funcionarios.view_cadastro'  # Permissão para visualizar objetos'

    def get_queryset(self):
        queryset = Cadastro.objects.filter(tenant=self.request.user.tenant)

        nome_funcionario_cadastro = self.request.GET.get('nome_funcionario')
        if nome_funcionario_cadastro:
            queryset = queryset.filter(id=nome_funcionario_cadastro)
        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')
        context['tenant'] = tenant

        # Paginação
        funcionarios = self.get_queryset().order_by('nome_funcionario')  # Ordena a lista de funcionários pelo nome
        paginator = Paginator(funcionarios, 10)  # Exibe 10 registros por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['funcionarios_list'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['query_params'] = self.request.GET.urlencode()

        # Adiciona os funcionários ao contexto para o form-select
        context['cadastros_funcionarios'] = self.get_queryset()
        return context


class CadastroCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    # campos que o usuario precisa preencher
    fields = ["nome_funcionario", "rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")
    permission_required = 'funcionarios.add_cadastro'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)  # Busca o tenant associado ao usuário
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('funcionarios_list', tenant)
    

class CadastroUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    fields = ["rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")
    permission_required = 'funcionarios.change_cadastro'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente, se necessário
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcionario'] = self.object  # Passa o objeto como 'funcionario'
        return context

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('funcionarios_list', tenant)


class ContratacaoListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin,ListView):
    model = Contratacao
    template_name = 'funcionarios/contratacao_list.html'  # Garante que o template correto será usado
    permission_required = 'funcionarios.view_contratacao'  # Permissão para visualizar objetos'

    def get_queryset(self):
        # Filtra as contratações com base no tenant do usuário
        tenant = getattr(self.request.user, 'tenant', None)
        queryset = Contratacao.objects.filter(tenant=tenant)

        # Captura os parâmetros da requisição GET
        data_inicio_contratacao = self.request.GET.get('data_inicio_contratacao')
        data_fim_contratacao = self.request.GET.get('data_fim_contratacao')

        # Aplica os filtros se os parâmetros estiverem presentes
        if data_inicio_contratacao:
            queryset = queryset.filter(data_contratacao__gte=data_inicio_contratacao)
        if data_fim_contratacao:
            queryset = queryset.filter(data_contratacao__lte=data_fim_contratacao)

        nome_funcionario_contratacao = self.request.GET.get('nome_funcionario')
        if nome_funcionario_contratacao:
            queryset = queryset.filter(id=nome_funcionario_contratacao)

        setor_contratacao = self.request.GET.get('setor')
        if setor_contratacao:
            queryset = queryset.filter(setor=setor_contratacao)

        cargo_contratacao = self.request.GET.get('cargo')
        if cargo_contratacao:
            queryset = queryset.filter(cargo=cargo_contratacao)

        # Usando Exists para verificar o status_rescisao (verifica se há uma rescisão associada)
        status_rescisao_subquery = Rescisao.objects.filter(nome_funcionario_id=OuterRef('nome_funcionario_id'))
        queryset = queryset.annotate(status_rescisao_exists=Exists(status_rescisao_subquery))

        # Filtrando quando o switch de status_rescisao for ativado
        filtrar_status_contrato = self.request.GET.get('filtrar_status_contrato')
        if filtrar_status_contrato == 'on':  # Quando o switch está ativado
            queryset = queryset.filter(status_rescisao_exists=False)  # Apenas contratações sem rescisão

        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')  # Formata o tenant
        context['tenant'] = tenant

        # Paginação
        funcionarios = self.get_queryset().order_by('nome_funcionario')  # Ordena a lista de funcionários pelo nome
        paginator = Paginator(funcionarios, 10)  # Exibe 10 registros por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['contratacao_funcionarios_paginados'] = page_obj
        # context['paginator'] = paginator
        # context['page_obj'] = page_obj
        # context['query_params'] = self.request.GET.urlencode()

        context['contratacao_funcionarios'] = Contratacao.objects.filter(tenant=self.request.user.tenant)
        context['contratacao_setor'] = Contratacao.objects.filter(tenant=self.request.user.tenant).values_list('setor', flat=True).distinct()
        context['contratacao_cargo'] = Contratacao.objects.filter(tenant=self.request.user.tenant).values_list('cargo', flat=True).distinct()
        context['filtrar_status_contrato'] = 'filtrar_status_contrato' in self.request.GET  # Passa o estado do switch para o template
        return context
    

class ContratacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Contratacao
    fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
                "contabilidade_admissional", "observacao_admissional"]
    success_url = reverse_lazy("contratacao_list")
    permission_required = 'funcionarios.add_contratacao'  # Permissão para visualizar objetos'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # IDs de funcionários que já foram contratados
            funcionarios_contratados_ids = Contratacao.objects.filter(tenant=tenant).values_list('nome_funcionario_id', flat=True)

            # IDs de funcionários que possuem rescisão
            funcionarios_com_rescisao_ids = Rescisao.objects.filter(tenant=tenant).values_list('nome_funcionario_id', flat=True)

            # IDs de funcionários a serem excluídos (contratados e com rescisão)
            ids_excluidos = set(funcionarios_contratados_ids) | set(funcionarios_com_rescisao_ids)

            # Filtra os funcionários disponíveis
            form.fields['nome_funcionario'].queryset = Cadastro.objects.filter(
                tenant=tenant
            ).exclude(id__in=ids_excluidos)
        else:
            form.fields['nome_funcionario'].queryset = Cadastro.objects.none()  # Retorna vazio se o tenant não for encontrado
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagamento_funcionarios'] = Pagamento.objects.filter(tenant=self.request.user.tenant)
        return context
    
    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant  # Atribui o tenant ao objeto antes de salvar
        return super().form_valid(form)
    
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('contratacao_list', tenant)


class ContratacaoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Contratacao
    # fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
    fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
              "contabilidade_admissional", "observacao_admissional"]

    # form_class = ContratacaoCreateView
    success_url = reverse_lazy("contratacao_list")
    permission_required = 'funcionarios.change_contratacao'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente, se necessário
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # Filtra os funcionários pelo tenant
            form.fields['nome_funcionario'].queryset = Cadastro.objects.filter(tenant=tenant)
        return form

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('contratacao_list', tenant)


class PagamentoListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Pagamento
    template_name = 'funcionarios/pagamento_list.html'
    permission_required = 'funcionarios.view_pagamento'  # Permissão para visualizar objetos'

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant', None)
        queryset = Pagamento.objects.filter(tenant=tenant).order_by('-data_pagamento')

        # Captura os parâmetros da requisição GET
        data_inicio_pagamento_funcionario = self.request.GET.get('data_inicio_pagamento_funcionario')
        data_fim_pagamento_funcionario = self.request.GET.get('data_fim_pagamento_funcionario')

        # Aplica os filtros se os parâmetros estiverem presentes
        if data_inicio_pagamento_funcionario:
            queryset = queryset.filter(data_pagamento__gte=data_inicio_pagamento_funcionario)
        if data_fim_pagamento_funcionario:
            queryset = queryset.filter(data_pagamento__lte=data_fim_pagamento_funcionario)

        nome_funcionario_pagamento = self.request.GET.get('nome_funcionario')
        if nome_funcionario_pagamento:
            queryset = queryset.filter(nome_funcionario_id=nome_funcionario_pagamento)

        tipo_pagamento = self.request.GET.get('tipo_pagamento')
        if tipo_pagamento:
            queryset = queryset.filter(tipo_pagamento=tipo_pagamento)

        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Paginação
        funcionarios = self.get_queryset()
        paginator = Paginator(funcionarios, 10)  # Exibe 10 registros por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['pagamento_funcionarios_paginados'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['query_params'] = self.request.GET.urlencode()


        # Adiciona dados adicionais ao contexto
        context['pagamento_funcionarios'] = Pagamento.objects.select_related('nome_funcionario').values('nome_funcionario_id', 'nome_funcionario__nome_funcionario').distinct()
        context['tipos_pagamento'] = Pagamento.objects.values_list('tipo_pagamento', flat=True).distinct()
        return context
    

class PagamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'funcionarios.add_pagamento'  # Permissão para visualizar objetos'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # IDs de funcionários com rescisão
            funcionarios_com_rescisao_ids = Rescisao.objects.filter(tenant=tenant).values_list('nome_funcionario_id', flat=True)

            # Filtra os funcionários contratados que não possuem rescisão
            form.fields['nome_funcionario'].queryset = Cadastro.objects.filter(
                tenant=tenant,
                contratacao__isnull=False  # Verifica se há uma contratação associada
            ).exclude(id__in=funcionarios_com_rescisao_ids).distinct()
        else:
            form.fields['nome_funcionario'].queryset = Cadastro.objects.none()  # Retorna vazio se o tenant não for encontrado
        return form

    def form_valid(self, form):
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)
        form.instance.tenant = tenant
        return super().form_valid(form)
    
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('pagamento_list', tenant)


class PagamentoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'funcionarios.change_pagamento'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente, se necessário
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        return super().form_valid(form)

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('pagamento_list', tenant)


class PagamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, DeleteView):
    model = Pagamento
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'pagamento.delete_payment'

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('pagamento_list', tenant)


class RescisaoListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Rescisao
    template_name = 'funcionarios/rescisao_list.html'
    permission_required = 'funcionarios.view_rescisao'  # Permissão para visualizar objetos'

    def get_queryset(self):
        queryset = Rescisao.objects.filter(tenant=self.request.user.tenant)

        # Captura os parâmetros da requisição GET
        data_inicio_rescisao = self.request.GET.get('data_inicio_rescisao')
        data_fim_rescisao = self.request.GET.get('data_fim_rescisao')

        # Aplica os filtros se os parâmetros estiverem presentes
        if data_inicio_rescisao:
            queryset = queryset.filter(data_desligamento__gte=data_inicio_rescisao)
        if data_fim_rescisao:
            queryset = queryset.filter(data_desligamento__lte=data_fim_rescisao)

        tipo_desligamento = self.request.GET.get('tipo_desligamento')
        if tipo_desligamento:
            queryset = queryset.filter(tipo_desligamento=tipo_desligamento)

        nome_funcionario_rescisao = self.request.GET.get('nome_funcionario')
        if nome_funcionario_rescisao:
            queryset = queryset.filter(id=nome_funcionario_rescisao)
        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')  # Formata o tenant
        context['tenant'] = tenant

        # Paginação
        funcionarios = self.get_queryset().order_by('-data_desligamento')  # Ordena a lista de funcionários pela data de desligamento
        paginator = Paginator(funcionarios, 10)  # Exibe 10 registros por página
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['rescisao_funcionarios_paginados'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['query_params'] = self.request.GET.urlencode()


        context['rescisao_funcionarios'] = Rescisao.objects.filter(tenant=self.request.user.tenant)
        context['tipo_desligamento'] = Rescisao.objects.values_list('tipo_desligamento', flat=True).distinct().filter(tenant=self.request.user.tenant)
        return context


class RescisaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Rescisao
    fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              ]
    success_url = reverse_lazy("rescisao_list")
    permission_required = 'funcionarios.add_rescisao'  # Permissão para visualizar objetos'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # IDs de funcionários que já possuem rescisão
            funcionarios_com_rescisao_ids = Rescisao.objects.filter(tenant=tenant).values_list('nome_funcionario_id', flat=True)

            # Filtra os funcionários contratados que ainda não possuem rescisão
            form.fields['nome_funcionario'].queryset = Cadastro.objects.filter(
                tenant=tenant,
                contratacao__isnull=False  # Verifica se há uma contratação associada
            ).exclude(id__in=funcionarios_com_rescisao_ids).distinct()
        else:
            form.fields['nome_funcionario'].queryset = Cadastro.objects.none()  # Retorna vazio se o tenant não for encontrado
        return form

    def form_valid(self, form):
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)
        form.instance.tenant = tenant
        return super().form_valid(form)

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('rescisao_list', tenant)
    

class RescisaoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Rescisao
    # fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
    fields = ["data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              ]
    success_url = reverse_lazy("rescisao_list")
    permission_required = 'funcionarios.change_rescisao'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente, se necessário
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        return super().form_valid(form)

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('rescisao_list', tenant)