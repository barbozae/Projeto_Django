from django.db import models
from users.models import Tenant
from django.conf import settings


class TaxasVendas(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)
    data_taxa_venda = models.DateField(verbose_name="Data", null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False)
    debito_mastercard = models.DecimalField(verbose_name="Débito MasterCard", max_digits=4, decimal_places=2, null=True, blank=True)
    debito_visa =models.DecimalField(verbose_name="Débito Visa", max_digits=4, decimal_places=2, null=True, blank=True)
    debito_elo =models.DecimalField(verbose_name="Débito Elo", max_digits=4, decimal_places=2, null=True, blank=True)
    credito_mastercard =models.DecimalField(verbose_name="Crédito MasterCard", max_digits=4, decimal_places=2, null=True, blank=True)
    credito_visa =models.DecimalField(verbose_name="Crédito Visa", max_digits=4, decimal_places=2, null=True, blank=True)
    credito_elo =models.DecimalField(verbose_name="Crédito Elo", max_digits=4, decimal_places=2, null=True, blank=True)
    hiper =models.DecimalField(verbose_name="Hiper", max_digits=4, decimal_places=2, null=True, blank=True)
    dinersclub =models.DecimalField(verbose_name="Dinersclub", max_digits=4, decimal_places=2, null=True, blank=True)
    american_express =models.DecimalField(verbose_name="American Express", max_digits=4, decimal_places=2, null=True, blank=True)
    alelo =models.DecimalField(verbose_name="Alelo", max_digits=4, decimal_places=2, null=True, blank=True)
    sodexo =models.DecimalField(verbose_name="Sodexo", max_digits=4, decimal_places=2, null=True, blank=True)
    vale_refeicao =models.DecimalField(verbose_name="Vale Refeição", max_digits=4, decimal_places=2, null=True, blank=True)
    ticket_rest =models.DecimalField(verbose_name="Ticket Rest", max_digits=4, decimal_places=2, null=True, blank=True)