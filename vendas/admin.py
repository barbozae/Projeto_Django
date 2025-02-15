from django.contrib import admin
from .models import Vendas


class VendasAdmin(admin.ModelAdmin):
    list_display = ('data_venda', 'periodo')

    #TODO esse search_fields não é tão interessante em vendas mas pode ser muito interessante em outras adimn
    search_fields = ('periodo',)


admin.site.register(Vendas, VendasAdmin)