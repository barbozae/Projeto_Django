from django.shortcuts import render
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.db import models
from django.core.cache import cache
from django.http import Http404
import time
from django.views.decorators.cache import cache_page


from .models import Vendas

from project.mixins import TenantQuerysetMixin, HandleNoPermissionMixin
from project.utils import generate_success_url


def vendas_resumo(request):
    return render(request, 'vendas/vendas_resume.html')


class VendasListView(LoginRequiredMixin, PermissionRequiredMixin, TenantQuerysetMixin, HandleNoPermissionMixin, ListView):
    model = Vendas
    template_name = 'vendas_list.html'  # Garante que o template correto será usado
    permission_required = 'vendas.view_vendas'  # Permissão para visualizar objetos'

    # def get_cache_key(self):
    #     tenant = getattr(self.request.user, 'tenant', None)
    #     if not tenant:
    #         return None  # Não usa cache se não houver tenant

    #     try:
    #         last_update = Vendas.objects.filter(tenant=tenant).aggregate(
    #             last=models.Max('dt_atualizado')
    #         )['last']
    #         last_update_str = str(last_update.timestamp()) if last_update else '1'
    #     except:
    #         # Fallback se houver algum erro
    #         last_update_str = '1'
        
    #     params = self.request.GET.urlencode()
    #     return f'venda_list_{tenant.id}_{last_update_str}_{params}'

    # @method_decorator(cache_page(60 * 15)) # Cache de 15 minutos
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        # queryset = Vendas.objects.filter(tenant=self.request.user.tenant)
        queryset = super().get_queryset()  # O TenantQuerysetMixin já filtra pelo tenant

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
        context = super().get_context_data(**kwargs)
        tenant = getattr(self.request.user, 'tenant', None)
        if tenant:
            tenant = str(tenant).lower().replace(' ', '_')
        context['tenant'] = tenant

        # Paginação
        vendas = context['object_list'].order_by('-data_venda')  # Lista de vendas do queryset
        paginator = Paginator(vendas, 10)  # 10 itens por página
        page_number = self.request.GET.get('page')  # Número da página atual
        vendas_page = paginator.get_page(page_number)

        context['vendas_list'] = vendas_page  # Lista paginada para o template

        # Cálculo de totais (baseado na lista paginada)
        venda_rodizio = 0
        venda_dinheiro = 0
        venda_pix = 0
        venda_debito = 0
        venda_credito = 0
        venda_beneficio = 0
        venda_total = 0

        for venda in vendas_page:  # Use somente os itens da página atual
            venda.debito = venda.calcular_debito()
            venda.credito = venda.calcular_credito()
            venda.beneficio = venda.calcular_beneficio()
            venda.total = venda.calcular_total()

            venda_rodizio += venda.rodizio or 0
            venda_dinheiro += venda.dinheiro or 0
            venda_pix += venda.pix or 0
            venda_debito += venda.debito or 0
            venda_credito += venda.credito or 0
            venda_beneficio += venda.beneficio or 0
            venda_total += venda.total

        # Adiciona os totais ao contexto
        context['vendas_rodizio'] = venda_rodizio
        context['vendas_dinheiro'] = venda_dinheiro
        context['vendas_pix'] = venda_pix
        context['vendas_debito'] = venda_debito
        context['vendas_credito'] = venda_credito
        context['vendas_beneficio'] = venda_beneficio
        context['vendas_total'] = venda_total

        return context


class VendasCreateView(LoginRequiredMixin, PermissionRequiredMixin, HandleNoPermissionMixin, CreateView):
    model = Vendas
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
             "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
             "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    permission_required = 'vendas.add_vendas'

    # NUNCA cache views de criação/edição
    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        tenant = getattr(self.request.user, 'tenant', None)
        if not tenant:
            return self.form_invalid(form)
        
        form.instance.tenant = tenant
        form.instance.author = self.request.user
        
        response = super().form_valid(form)
        
        # Invalida o cache da listagem após criar
        self._invalidate_vendas_cache(tenant)
        
        return response

    # refresh faz com que os cache sejam ignorados
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        base_url = reverse('venda_list')
        # Adiciona parâmetro para forçar atualização
        return f"{base_url}?tenant={tenant}&refresh=true" if tenant else base_url

    # def _invalidate_vendas_cache(self, tenant):
    #     """Invalida o cache da listagem de vendas para o tenant específico"""
    #     try:
    #         cache_key_pattern = f'venda_list_{tenant.id}_*'
            
    #         # Tenta deletar usando padrão (Redis)
    #         try:
    #             cache.delete_pattern(cache_key_pattern)
    #             return
    #         except (AttributeError, NotImplementedError):
    #             pass
                
    #         # Fallback para outros backends
    #         keys_to_delete = []
    #         for key in cache._cache.iterkeys():  # Adapte conforme seu backend
    #             if str(key).startswith(f'venda_list_{tenant.id}_'):
    #                 keys_to_delete.append(key)
            
    #         if keys_to_delete:
    #             cache.delete_many(keys_to_delete)
                
    #     except Exception as e:
    #         import logging
    #         logger = logging.getLogger(__name__)
    #         logger.error(f"Erro ao invalidar cache: {str(e)}")


class VendasUpDateView(LoginRequiredMixin, PermissionRequiredMixin, HandleNoPermissionMixin, UpdateView):
    model = Vendas
    fields = ["data_venda", "periodo", "rodizio", "dinheiro", "pix", "debito_mastercard", "debito_visa", 
              "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "alelo", "american_express",
              "hiper", "sodexo", "ticket_rest", "vale_refeicao", "dinersclub", "socio"]
    success_url = reverse_lazy("venda_list")
    permission_required = 'vendas.change_vendas'

    # @method_decorator(never_cache)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Adiciona o usuário logado como autor
        form.instance.author = self.request.user
        return super().form_valid(form)

    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('venda_list', tenant)


class VendasDeleteView(LoginRequiredMixin, PermissionRequiredMixin, HandleNoPermissionMixin, DeleteView):
    model = Vendas
    success_url = reverse_lazy("venda_list")
    permission_required = 'vendas.delete_vendas'

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # get_success_url é um método que retorna a URL de sucesso após a operação
    def get_success_url(self):
        tenant = getattr(self.request.user, 'tenant', None)
        return generate_success_url('venda_list', tenant)