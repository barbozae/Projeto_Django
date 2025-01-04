from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .models import Fornecedor, Compras


class FornecedorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedor_list.html'  # Garante que o template correto será usado
    permission_required = 'compras.view_fornecedor'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    

class FornecedorCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Fornecedor
    # campos que o usuario precisa preencher
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.add_fornecedor'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class FornecedorUpDateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Fornecedor
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.change_fornecedor'  # Permissão para visualizar objetos'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class ComprasListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    model = Compras
    permission_required = 'compras.view_compras'  # Permissão para visualizar objetos'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    

class ComprasCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Compras
    # campos que o usuario precisa preencher
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'compras.add_compras'  # Permissão para visualizar objetos'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class ComprasUpDateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Compras
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.change_compras'  # Permissão para visualizar objetos'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
    


class ComprasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Compras
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.delete_compras'  # Permissão para visualizar objetos'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão