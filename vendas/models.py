from django.db import models
from users.models import Tenant
from django.conf import settings

class Vendas(models.Model):
    PERIODO_CHOICES = [
        ('Almoço', 'Almoço'),
        ('Jantar', 'Jantar'),
        ]
    
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

    def save(self, *args, **kwargs):
        if not self.tenant_id:
            self.tenant = kwargs.pop('tenant', None)
        if not self.author_id :  # Verifica se o autor não foi definido
            self.author = kwargs.pop('user', None)  # Pega o usuário da kwargs
        super().save(*args, **kwargs)

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