from django.contrib import admin
from .models import Cadastro, Contratacao, Pagamento, Rescisao


# Register your models here.
class CadastroAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "rg", "cpf", "carteira_trabalho", "endereco", "numero", "bairro", "cidade",
                    "telefone", "banco", "agencia", "conta"]


class ContratacaoAdmin(admin.ModelAdmin):
    list_display = ["nome_funcionario", "cargo", "setor", "data_exame_admissional", "data_contratacao", "salario",
                  "documentacao_admissional", "contabilidade_admissional", "status_admissional", "observacao_admissional"]


admin.site.register(Cadastro, CadastroAdmin)
admin.site.register(Contratacao, ContratacaoAdmin)