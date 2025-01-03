from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # validação da permissão do usuário

from .models import Vendas


def vendas_resumo(request):
    return render(request, 'vendas/vendas_resume.html')

# Função para verificar se o usuário é membro da equipe
def is_team_member(user):
    # Verifica se o usuário é um superusuário ou se é membro do grupo 'Equipe'
    return user.is_superuser or user.groups.filter(name='Vendas').exists()

class VendasListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
# class VendasListView(ListView):
    model = Vendas
    template_name = 'vendas_list.html'  # Garante que o template correto será usado

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

    # Avaliar se usuário tem acesso a view retornando True ou False
    def test_func(self):
        return is_team_member(self.request.user)

    # Caso a função test_func retorna False essa função redireciona para home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()  # Redireciona para a página de login
        return redirect('home')  # Redireciona para home se não for membro da equipe


class VendasCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
# class VendasCreateView(CreateView):
    model = Vendas
    # campos que o usuario precisa preencher
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
              "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
              "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("venda_list")

    def form_valid(self, form):
        # Adiciona o usuário logado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Avaliar se usuário tem acesso a view retornando True ou False
    def test_func(self):
        return is_team_member(self.request.user)

    # Caso a função test_func retorna False essa função redireciona para home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return redirect('home')


class VendasUpDateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# class VendasUpDateView(UpdateView):
    model = Vendas
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
              "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
              "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    success_url = reverse_lazy("venda_list")

    def form_valid(self, form):
        # Adiciona o usuário logado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # Avaliar se usuário tem acesso a view retornando True ou False
    def test_func(self):
        return is_team_member(self.request.user)

    # Caso a função test_func retorna False essa função redireciona para home
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return redirect('home')


class VendasDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
# class VendasDeleteView(DeleteView):
    model = Vendas
    success_url = reverse_lazy("venda_list")

    def test_func(self):
        return is_team_member(self.request.user)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return redirect('home')
