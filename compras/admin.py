from django.contrib import admin
from .models import Fornecedor, Compras


class FornecedorAdmin(admin.ModelAdmin):
    list_display = ["nome_empresa", "tenant", "cnpj", "nome_contato", "telefone", "email", "bairro", "cidade",
                    "endereco", "cep", "numero"]


class ComprasAdmin(admin.ModelAdmin):
    list_display = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", 
                    "valor_pago", "qtd", "numero_boleto", "grupo_produto", "produto", "classificacao",
                    "forma_pagamento", "observacao"]

    def get_queryset(self, request):
        # Se o usuário for superusuário, retorna todos os registros
        if request.user.is_superuser:
            return Compras.objects.all()
        
        # Caso contrário, filtra pelos registros do tenant atual
        tenant = getattr(request, 'tenant', None)
        if tenant is None:
            return Compras.objects.none()  # Nenhum registro caso o tenant não seja encontrado
        
        return Compras.objects.filter(tenant=tenant)


# Registro de Cadastro explícito
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Compras, ComprasAdmin)
