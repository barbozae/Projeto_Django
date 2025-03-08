from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Cadastro, Contratacao, Pagamento, Rescisao




#TODO não permitir realizar rescisão do mesmo ID mais de uma vez




class CadastroListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_list.html'  # Garante que o template correto será usado
    context_object_name = 'funcionarios_list'
    permission_required = 'funcionarios.view_cadastro'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    
    def get_queryset(self):
        queryset = Cadastro.objects.all()

        nome_funcionario_cadastro = self.request.GET.get('nome_funcionario')
        if nome_funcionario_cadastro:
            queryset = queryset.filter(id=nome_funcionario_cadastro)
        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cadastros_funcionarios'] = Cadastro.objects.all()
        return context


class CadastroCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    # campos que o usuario precisa preencher
    fields = ["nome_funcionario", "rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")
    permission_required = 'funcionarios.add_cadastro'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class CadastroUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    fields = ["rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")
    permission_required = 'funcionarios.change_cadastro'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcionario'] = self.object  # Passa o objeto como 'funcionario'
        return context


class ContratacaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Contratacao
    template_name = 'funcionarios/contratacao_list.html'  # Garante que o template correto será usado
    permission_required = 'funcionarios.view_contratacao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    
    def get_queryset(self):
        queryset = Contratacao.objects.all()

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
            queryset = queryset.filter(id=setor_contratacao)

        cargo_contratacao = self.request.GET.get('cargo')
        if cargo_contratacao:
            queryset = queryset.filter(id=cargo_contratacao)

        # Verifica se há rescisão para cada contratação
        # for contratacao in queryset:
        #     rescisao = Rescisao.objects.filter(nome_funcionario_id=contratacao.nome_funcionario_id).first()
        #     contratacao.status_rescisao = rescisao.status_rescisao if rescisao else False

        # Adiciona o campo status_rescisao a cada objeto contratacao
        # rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        # for contratacao in queryset:
        #     contratacao.status_rescisao = contratacao.pk in rescisao_ids
            
        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contratacao_funcionarios'] = Contratacao.objects.all()
        context['contratacao_setor'] = Contratacao.objects.all()
        context['contratacao_cargo'] = Contratacao.objects.all()
        return context


class ContratacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Contratacao
    fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
                "contabilidade_admissional", "observacao_admissional"]
    success_url = reverse_lazy("contratacao_list")
    permission_required = 'funcionarios.add_contratacao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    
    # com essas duas funções abaixo eu tenho apenas a lista de funcionarios que não foram cadastrados
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários cadastrados que não foram contratados ainda
        contratacao_ids = Contratacao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Cadastro.objects.exclude(id__in=contratacao_ids)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagamento_funcionarios'] = Pagamento.objects.all()
        return context


class ContratacaoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contratacao
    # fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
    fields = ["setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
              "contabilidade_admissional", "observacao_admissional"]
    
    # form_class = ContratacaoCreateView
    success_url = reverse_lazy("contratacao_list")
    permission_required = 'funcionarios.change_contratacao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários que não foram contratados
        # rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        contratacao_ids = Contratacao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Cadastro.objects.exclude(id__in=contratacao_ids)
        return form


class PagamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pagamento
    template_name = 'funcionarios/pagamento_list.html'
    permission_required = 'funcionarios.view_pagamento'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_queryset(self):
        queryset = Pagamento.objects.all()

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
            queryset = queryset.filter(id=nome_funcionario_pagamento)

        tipo_pagamento = self.request.GET.get('tipo_pagamento')
        if tipo_pagamento:
            queryset = queryset.filter(id=tipo_pagamento)

        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagamento_funcionarios'] = Pagamento.objects.all()
        return context
    

class PagamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'funcionarios.add_pagamento'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários com base nas contratações que não foram rescindidas
        rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Contratacao.objects.exclude(nome_funcionario_id__in=rescisao_ids)
        return form


class PagamentoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'funcionarios.change_pagamento'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários com base nas contratações que não foram rescindidas
        rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Contratacao.objects.exclude(nome_funcionario_id__in=rescisao_ids)
        return form


class PagamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Pagamento
    success_url = reverse_lazy("pagamento_list")
    permission_required = 'pagamento.delete_payment'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class RescisaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Rescisao
    template_name = 'funcionarios/rescisao_list.html'
    permission_required = 'funcionarios.view_rescisao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_queryset(self):
        queryset = Rescisao.objects.all()

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
            queryset = queryset.filter(id=tipo_desligamento)

        nome_funcionario_rescisao = self.request.GET.get('nome_funcionario')
        if nome_funcionario_rescisao:
            queryset = queryset.filter(id=nome_funcionario_rescisao)
        return queryset

    # com essa função eu tenho a lista completa de funcionarios mesmo com filtro
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rescisao_funcionarios'] = Rescisao.objects.all()
        return context


class RescisaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Rescisao
    fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              ]
    success_url = reverse_lazy("rescisao_list")
    permission_required = 'funcionarios.add_rescisao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários com base nas contratações que não foram rescindidas
        rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Contratacao.objects.exclude(nome_funcionario_id__in=rescisao_ids)
        return form


class RescisaoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Rescisao
    fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              ]
    success_url = reverse_lazy("rescisao_list")
    permission_required = 'funcionarios.change_rescisao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra os funcionários com base nas contratações que não foram rescindidas
        rescisao_ids = Rescisao.objects.values_list('nome_funcionario_id', flat=True)
        form.fields['nome_funcionario'].queryset = Contratacao.objects.exclude(nome_funcionario_id__in=rescisao_ids)
        return form