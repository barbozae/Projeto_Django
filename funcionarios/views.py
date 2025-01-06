from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Cadastro, Contratacao, Pagamento, Rescisao


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


class ContratacaoUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Contratacao
    fields = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
              "contabilidade_admissional", "observacao_admissional"]
    
    # form_class = ContratacaoCreateView
    success_url = reverse_lazy("contratacao_list")
    permission_required = 'funcionarios.change_contratacao'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class PagamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Pagamento
    template_name = 'funcionarios/pagamento_list.html'
    permission_required = 'funcionarios.view_pagamento'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


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