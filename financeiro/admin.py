from django.contrib import admin
from .models import TaxasVendas


class TaxasVendasAdmin(admin.ModelAdmin):
    list_display = (["tenant", "created_at", "dt_atualizado", "data_taxa_venda", "debito_mastercard",
                     "debito_visa", "debito_elo", "credito_mastercard", "credito_visa", "credito_elo", "hiper",
                     "dinersclub", "american_express", "alelo", "sodexo", "vale_refeicao", "ticket_rest", "author"])

    #TODO esse search_fields não é tão interessante em vendas mas pode ser muito interessante em outras adimn
    search_fields = ('tenant',)


admin.site.register(TaxasVendas, TaxasVendasAdmin)