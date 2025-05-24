from django.conf import settings
from django.db import models
from users.models import Tenant


class Fornecedor(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    nome_empresa = models.CharField(verbose_name="Fornecedor", max_length=50, blank=False)
    cnpj = models.CharField(verbose_name="CNPJ", max_length=14, null=True, blank=True)
    nome_contato = models.CharField(verbose_name="Contato", max_length=35, null=True, blank=True)
    telefone = models.CharField(verbose_name="Telefone", max_length=15, null=True, blank=True)
    email = models.CharField(verbose_name="E-mail", max_length=40, null=True, blank=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=255, null=True, blank=True)
    cep = models.CharField(verbose_name="CEP", max_length=8, null=True, blank=True)
    numero = models.CharField(verbose_name="Número", max_length=10, null=True, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=20, null=True, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=30, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    # garantir que nome da empresa seja único para cada tenant
    class Meta:
        unique_together = ('tenant', 'nome_empresa')
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"

    def __str__(self):
        # Retorna uma string representando o fornecedor
        return f"{self.nome_empresa}"
        # return f"{self.nome_empresa} - {self.cnpj if self.cnpj else 'CNPJ não informado'}"

    
class Compras(models.Model):
    classificacao_choices = [
                        ('CMV', 'CMV'),
                        ('Gasto Fixo', 'Gasto Fixo'),
                        ('Gasto Variável', 'Gasto Variável')
                        ]
    tipo_pagamento = [
                    ('Dinheiro', 'Dinheiro'),
                    ('Cartão de Crédito', 'Cartão de Crédito'),
                    ('Cartão Débito', 'Cartão Débito'),
                    ('Pix', 'Pix'),
                    ('Cheque', 'Cheque'),
                    ('Transferência', 'Transferência'),
                    ('Boleto', 'Boleto'),
                    ('Débito Automático', 'Débito Automático')
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data_compra = models.DateField(verbose_name="Data da Venda", null=False, blank=False)
    data_vencimento = models.DateField(verbose_name="Data do Vencimento", null=True, blank=False)
    data_pagamento = models.DateField(verbose_name="Data do Pagamento", null=True, blank=True)
    # Chave estrangeira para Fornecedor, associando a PK de Fornecedor
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name="Fornecedor", null=False, blank=False)
    valor_compra = models.DecimalField(verbose_name="Valor da Compra", max_digits=9, decimal_places=2, null=False, blank=False)
    valor_pago = models.DecimalField(verbose_name="Valor de Pagamento", max_digits=9, decimal_places=2, null=True, blank=True)
    qtd = models.CharField(verbose_name="Quantidade", max_length=10, null=True, blank=True)
    numero_boleto = models.CharField(verbose_name="Boleto", max_length=10, null=True, blank=True)
    grupo_produto = models.CharField(verbose_name="Grupo do Produto", max_length=20, null=True, blank=False)
    produto = models.CharField(verbose_name="Produto", max_length=20, null=True, blank=False)
    classificacao = models.CharField(verbose_name="Classificação", choices=classificacao_choices, max_length=20, null=True, blank=False)
    forma_pagamento = models.CharField(verbose_name="Forma de Pagamento", choices=tipo_pagamento, max_length=17, null=True, blank=False)
    observacao = models.CharField(verbose_name="Observação", max_length=35, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, default=1)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)