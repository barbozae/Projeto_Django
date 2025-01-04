from django.contrib import admin
from .models import Fornecedor, Compras


class FornecedorAdmin(admin.ModelAdmin):
    list_display = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email", "bairro", "cidade",
                    "endereco", "cep", "numero"]


class ComprasAdmin(admin.ModelAdmin):
    list_display = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", 
                    "valor_pago", "qtd", "numero_boleto", "grupo_produto", "produto", "classificacao",
                    "forma_pagamento", "observacao"]


# Registro de Cadastro explícito
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Compras, ComprasAdmin)