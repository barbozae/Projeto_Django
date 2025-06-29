from django.db import models
from users.models import Tenant
from django.conf import settings
from django.core.cache import cache
import logging


class Vendas(models.Model):
    PERIODO_CHOICES = (
        ('Almoço', 'Almoço'),
        ('Jantar', 'Jantar'),
    )
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data_venda = models.DateField(verbose_name="Data da Venda", null=False, blank=False)
    periodo = models.CharField(verbose_name="Período", max_length=6, choices=PERIODO_CHOICES, blank=False)
    rodizio = models.IntegerField(verbose_name="Qtd Rodízio", null=False, blank=False)
    dinheiro = models.DecimalField(verbose_name="Dinheiro", max_digits=8, decimal_places=2, null=True, blank=True)
    pix = models.DecimalField(verbose_name="Pix", max_digits=8, decimal_places=2, null=True, blank=True)
    debito_mastercard = models.DecimalField(verbose_name="Debito MasterCard", max_digits=8, decimal_places=2, null=True, blank=True)
    debito_visa = models.DecimalField(verbose_name="Debito Visa", max_digits=8, decimal_places=2, null=True, blank=True)
    debito_elo = models.DecimalField(verbose_name="Debito Elo", max_digits=8, decimal_places=2, null=True, blank=True)
    credito_mastercard = models.DecimalField(verbose_name="Credito MasterCard", max_digits=8, decimal_places=2, null=True, blank=True)
    credito_visa = models.DecimalField(verbose_name="Credito Visa", max_digits=8, decimal_places=2, null=True, blank=True)
    credito_elo = models.DecimalField(verbose_name="Credito Elo", max_digits=8, decimal_places=2, null=True, blank=True)
    alelo = models.DecimalField(verbose_name="Alelo", max_digits=8, decimal_places=2, null=True, blank=True)
    american_express = models.DecimalField(verbose_name="Amex", max_digits=8, decimal_places=2, null=True, blank=True)
    hiper = models.DecimalField(verbose_name="HiperCard", max_digits=8, decimal_places=2, null=True, blank=True)
    sodexo = models.DecimalField(verbose_name="Sodexo", max_digits=8, decimal_places=2, null=True, blank=True)
    ticket_rest = models.DecimalField(verbose_name="Ticket Refeição", max_digits=8, decimal_places=2, null=True, blank=True)
    vale_refeicao = models.DecimalField(verbose_name="Vale Refeição", max_digits=8, decimal_places=2, null=True, blank=True)
    dinersclub = models.DecimalField(verbose_name="DinersClub", max_digits=8, decimal_places=2, null=True, blank=True)
    socio = models.DecimalField(verbose_name="Sócio", max_digits=8, decimal_places=2, null=True, blank=True)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False)

    # class excencial para os caches
    class Meta:
        get_latest_by = 'dt_atualizado'

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            self.tenant = kwargs.pop('tenant', None)
        if not self.author_id :  # Verifica se o autor não foi definido
            self.author = kwargs.pop('user', None)  # Pega o usuário da kwargs
        super().save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     # Lógica existente de tenant e author
    #     if not self.tenant_id:
    #         self.tenant = kwargs.pop('tenant', None)
    #     if not self.author_id:
    #         self.author = kwargs.pop('user', None)
    #     # Executa o save normal
    #     super().save(*args, **kwargs)
    #     # Invalida o cache após o save
    #     self._invalidate_vendas_cache()
        
    # def _invalidate_vendas_cache(self):
    #     # Invalida o cache da listagem de vendas
    #     try:
    #         if not hasattr(self, 'tenant') or not self.tenant:
    #             return
                
    #         tenant_id = str(self.tenant.id)
    #         cache_key_pattern = f'venda_list_{tenant_id}_*'
            
    #         # Tenta deletar usando padrão (Redis)
    #         try:
    #             cache.delete_pattern(cache_key_pattern)
    #             return
    #         except (AttributeError, NotImplementedError):
    #             pass
                
    #         # Fallback para backends que não suportam delete_pattern
    #         from django.core.cache.utils import make_template_fragment_key
    #         keys_to_delete = []
            
    #         # Adiciona chave principal
    #         keys_to_delete.append(make_template_fragment_key('venda_list'))
            
    #         # Tenta encontrar outras variações
    #         try:
    #             for key in cache._cache.iterkeys():  # Adapte conforme seu backend
    #                 if isinstance(key, str) and key.startswith(f'venda_list_{tenant_id}_'):
    #                     keys_to_delete.append(key)
    #         except AttributeError:
    #             pass
                
    #         if keys_to_delete:
    #             cache.delete_many(list(set(keys_to_delete)))
                
    #     except Exception as e:
    #         import logging
    #         logger = logging.getLogger(__name__)
    #         logger.error(f"Erro ao invalidar cache de vendas: {str(e)}", exc_info=True)


    def calcular_debito(self):
        return (self.debito_mastercard or 0) + (self.debito_visa or 0) + (self.debito_elo or 0)

    def calcular_credito(self):
        return (self.credito_mastercard or 0) + (self.credito_visa or 0) + (self.credito_elo or 0)

    def calcular_beneficio(self):
        return (
            (self.alelo or 0) + 
            (self.american_express or 0) +
            (self.hiper or 0) + 
            (self.sodexo or 0) + 
            (self.ticket_rest or 0) + 
            (self.vale_refeicao or 0) + 
            (self.dinersclub or 0)
        )

    def calcular_total(self):
        return (
            (self.dinheiro or 0) +
            (self.pix or 0) +
            self.calcular_debito() +
            self.calcular_credito() +
            self.calcular_beneficio()
        )
    
    def __str__(self):
        # Retorna a data no formato desejado
        return self.data_venda.strftime("%d/%m/%Y")