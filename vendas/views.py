from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Vendas


def vendas_resumo(request):
    return render(request, 'vendas/vendas_resume.html')

class VendasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vendas
    template_name = 'vendas_list.html'  # Garante que o template correto será usado
    permission_required = 'vendas.view_vendas'  # Permissão para visualizar objetos'

    def get_queryset(self):
        queryset = Vendas.objects.all()

        # Filtra pelo intervalo de datas, se os parâmetros de data foram passados
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        periodo = self.request.GET.get('periodo')

        if data_inicio:
            queryset = queryset.filter(data_venda__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_venda__lte=data_fim)
        if periodo:
            queryset = queryset.filter(periodo=periodo)

        return queryset

    def get_context_data(self, **kwargs):
        # Recupera o contexto padrão do Django
        context = super().get_context_data(**kwargs)

        # Inicializa o total_geral
        total_geral = 0  # Inicializa antes de usar

        # Calculando os totais usando os métodos do modelo
        vendas = context['object_list']
        for venda in vendas:
            venda.debito = venda.calcular_debito()
            venda.credito = venda.calcular_credito()
            venda.beneficio = venda.calcular_beneficio()
            venda.total = venda.calcular_total()

            # somando todas as linhas
            total_geral += venda.total
        
        # Adiciona o total geral ao contexto
        context['vendas_total'] = total_geral
        return context

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class VendasCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Vendas
    # campos que o usuario precisa preencher
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
              "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
              "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("venda_list")
    permission_required = 'vendas.add_vendas'

    def form_valid(self, form):
        # Adiciona o usuário logado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class VendasUpDateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Vendas
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
              "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
              "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    success_url = reverse_lazy("venda_list")
    permission_required = 'vendas.change_vendas'

    def form_valid(self, form):
        # Adiciona o usuário logado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão


class VendasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Vendas
    success_url = reverse_lazy("venda_list")
    permission_required = 'vendas.delete_vendas'

    # caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão
