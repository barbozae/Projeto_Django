# from urllib.parse import quote  # para codificar o tenant corretamente

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Fornecedor, Compras
from project.mixins import TenantQuerysetMixin, HandleNoPermissionMixin
from project.utils import generate_success_url


class FornecedorListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Fornecedor
    template_name = 'fornecedor_list.html'  # Garante que o template correto será usado
    permission_required = 'compras.view_fornecedor'  # Permissão para visualizar objetos'

    def get_queryset(self):
        # Obtém o tenant do usuário logado
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return Fornecedor.objects.none()  # Retorna vazio se o tenant não for encontrado

        # Filtra os fornecedores pelo tenant
        queryset = Fornecedor.objects.filter(tenant=tenant)

        # Captura os parâmetros da requisição GET
        nome_empresa = self.request.GET.getlist('nome_empresa[]')

        # Aplica o filtro de nome_empresa apenas se houver valores válidos
        nome_empresa = [nome for nome in nome_empresa if nome.strip()]  # Remove valores vazios e espaços
        if nome_empresa:
            queryset = queryset.filter(nome_empresa__in=nome_empresa)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')  # Converte para minúsculas e substitui espaços por underscores
        context['tenant'] = tenant

        #Filtrar os fornecedores com base no tenant
        context['fornecedores'] = Fornecedor.objects.filter(tenant=self.request.user.tenant)
        # context['numero_boleto'] = Compras.objects.values_list('numero_boleto', flat=True).distinct()
        context['numero_boleto'] = Compras.objects.filter(tenant=self.request.user.tenant).values_list('numero_boleto', flat=True).distinct()
        return context
    

class FornecedorCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Fornecedor
    # campos que o usuario precisa preencher
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.add_fornecedor'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)  # Busca o tenant associado ao usuário
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('fornecedor_list', tenant)


class FornecedorUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Fornecedor
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    success_url = reverse_lazy("fornecedor_list")
    permission_required = 'compras.change_fornecedor'  # Permissão para visualizar objetos'

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('fornecedor_list', tenant)


class ComprasListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    def compras_list(request):
        if not request.tenant:
            return render(request, 'error.html', {"message": "Tenant not found"})

    model = Compras
    permission_required = 'compras.view_compras'  # Permissão para visualizar objetos'

    def get_queryset(self):
        # Obtém o tenant do usuário logado
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return Compras.objects.none()  # Retorna vazio se o tenant não for encontrado
    
        # queryset = Compras.objects.all()
        # Filtra as compras pelo tenant
        queryset = Compras.objects.filter(tenant=tenant)

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
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')  # Converte para minúsculas e substitui espaços por underscores
        context['tenant'] = tenant

        # Filtra os fornecedores e boletos pelo tenant
        context['fornecedores'] = Fornecedor.objects.filter(tenant=self.request.user.tenant)
        context['numero_boleto'] = Compras.objects.filter(tenant=self.request.user.tenant).values_list('numero_boleto', flat=True).distinct()

        return context
    

class ComprasCreateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, CreateView):
    model = Compras
    # campos que o usuario precisa preencher
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'compras.add_compras'  # Permissão para visualizar objetos'

    def form_valid(self, form):
        # Certifique-se de que o tenant está sendo atribuído corretamente
        tenant = getattr(self.request.user, 'tenant', None)  # Busca o tenant associado ao usuário
        if not tenant:
            return self.form_invalid(form)  # Retorna erro se o tenant não for encontrado
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Filtra os fornecedores pelo tenant no formulário de criação
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # Filtra os fornecedores pelo tenant
            form.fields['fornecedor'].queryset = Fornecedor.objects.filter(tenant=tenant)
        return form

    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)


class ComprasUpDateView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, UpdateView):
    model = Compras
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.change_compras'  # Permissão para visualizar objetos'

    # Filtra os fornecedores pelo tenant no formulário de criação
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            # Filtra os fornecedores pelo tenant
            form.fields['fornecedor'].queryset = Fornecedor.objects.filter(tenant=tenant)
        return form

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)
    

class ComprasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, DeleteView):
    model = Compras
    success_url = reverse_lazy("compras_list")
    permission_required = 'socio.delete_compras'  # Permissão para visualizar objetos'

    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('compras_list', tenant)