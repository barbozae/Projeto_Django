from django.contrib import admin
from .models import Cadastro, Contratacao, Pagamento, Rescisao


class CadastroAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "rg", "cpf", "carteira_trabalho", "endereco", "numero", "bairro", "cidade",
                    "telefone", "banco", "agencia", "conta"]


class ContratacaoAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "setor", "cargo", "data_exame_admissional", "data_contratacao", "salario",
                  "documentacao_admissional", "contabilidade_admissional", "status_admissional", "observacao_admissional"]


class PagamentoAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]


class RescisaoAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
                    "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
                     "status_rescisao"]


# Registro de Cadastro explícito
admin.site.register(Cadastro, CadastroAdmin)
admin.site.register(Contratacao, ContratacaoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Rescisao, RescisaoAdmin)