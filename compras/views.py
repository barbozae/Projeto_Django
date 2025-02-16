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

    def get_queryset(self):
        queryset = Fornecedor.objects.all()

        # Captura os parâmetros da requisição GET
        nome_empresa = self.request.GET.getlist('nome_empresa[]')
        
        # Aplica o filtro de nome_empresa apenas se houver valores válidos
        nome_empresa = [nome for nome in nome_empresa if nome.strip()]  # Remove valores vazios e espaços
        if nome_empresa:
            queryset = queryset.filter(nome_empresa__in=nome_empresa)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedores'] = Fornecedor.objects.all()
        return context
    

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
    
    def get_queryset(self):
        queryset = Compras.objects.all()

        # Captura os parâmetros da requisição GET
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        fornecedor_selecionado = self.request.GET.getlist('fornecedor[]')
        boleto_selecionado = self.request.GET.getlist('numero_boleto[]')

        # Aplica os filtros se os parâmetros estiverem presentes
        if data_inicio:
            queryset = queryset.filter(data_compra__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_compra__lte=data_fim)

        # Aplica o filtro de fornecedor apenas se houver fornecedores selecionados e ignora valores vazios
        fornecedor_selecionado = [f for f in fornecedor_selecionado if f]  # Remove valores vazios
        if fornecedor_selecionado:  # Só aplica o filtro se a lista não estiver vazia
            queryset = queryset.filter(fornecedor__id__in=fornecedor_selecionado)

        boleto_selecionado = [b for b in boleto_selecionado if b]  # Remove valores vazios
        if boleto_selecionado:
            # boleto_selecionado = [b for b in boleto_selecionado if b and b != "None"]
            queryset = queryset.filter(numero_boleto__in=boleto_selecionado)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fornecedores'] = Fornecedor.objects.all()
        context['numero_boleto'] = Compras.objects.values_list('numero_boleto', flat=True).distinct()
        return context
    

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