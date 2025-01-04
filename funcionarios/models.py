from django.contrib.auth.models import User
from django.db import models


class Cadastro(models.Model):
    lista_banco = [('Banco do Brasil', 'Banco do Brasil'),
                   ('Banco Original', 'Banco Original'),
                   ('Bradesco', 'Bradesco'),
                   ('Caixa Econômica', 'Caixa Econômica'),
                   ('C6 Bank', 'C6 Bank'),
                   ('Itau', 'Itau'),
                   ('Inter', 'Inter'),
                   ('Neon', 'Neon'),
                   ('Next', 'Next'),
                   ('Nubank', 'Nubank'),
                   ('Santander', 'Santander'),
                   ]
    
    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.CharField(verbose_name="Funcionário", max_length=40 , blank=False, unique=True)
    rg = models.CharField(verbose_name="RG", max_length=14, null=True , blank=True)
    cpf = models.CharField(verbose_name="CPF", max_length=14, null=True , blank=True)
    carteira_trabalho = models.CharField(verbose_name="Carteira Trabalho", max_length=12, null=True, blank=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=40, null=True, blank=True)
    numero = models.CharField(verbose_name="Número", max_length=255, null=True, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=20, null=True, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=30, null=True, blank=True)
    telefone = models.CharField(verbose_name="Telefone", max_length=13, null=True, blank=True)
    banco = models.CharField(verbose_name="Banco", choices=lista_banco, max_length=15, null=True, blank=True)
    agencia = models.CharField(verbose_name="Agencia", max_length=7, null=True, blank=True)
    conta = models.CharField(verbose_name="Conta", max_length=10, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        # Retorna uma string representando o funcionário devido a ForeignKey em PG_Funcionarios
        return f"{self.nome_funcionario}"


class Contratacao(models.Model):
    cargos_por_setor = {
                    'Administração': ["Gerente Financeiro", "Auxiliar Adm"],
                    'Cozinha': ["Chef", "Cozinheiro", "Cozinheiro Auxiliar"],
                    'Limpeza': ["Faxineira(o)"],
                    'Sushi': ["Peixeiro", "Sushiman", "Sushiman Auxiliar"],
                    'Salão': ["Caixa", "Cumin", "Garçom", "Gerente Geral", "Maitre", "Recepcionista"],
                    'Bar': ["Barman", "Copeiro"],
                    'Vallet': ["Manobrista"]
                    }
    
    SETOR_CHOICES = [(key, key) for key in cargos_por_setor.keys()]
    CARGO_CHOICES = [(value, value) for sublist in cargos_por_setor.values() for value in sublist]

    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    setor = models.CharField(verbose_name="Setor", choices=SETOR_CHOICES, max_length=13, null=False, blank=False)
    cargo = models.CharField(verbose_name="Cargo", choices=CARGO_CHOICES, max_length=19, null=False, blank=False)
    data_exame_admissional = models.DateField(verbose_name="Dt Exame Admissional", null=True, blank=True)
    data_contratacao = models.DateField(verbose_name="Data Contratação", null=False, blank=False)
    salario = models.DecimalField(verbose_name="Salário", max_digits=9, decimal_places=2, null=True, blank=True)
    documentacao_admissional = models.CharField(verbose_name="Doc Admissional", max_length=10, null=True, blank=True)
    contabilidade_admissional = models.CharField(verbose_name="Doc Contabilidade", max_length=10, null=True, blank=True)
    status_admissional = models.CharField(verbose_name="Status Admissão", max_length=10, null=True, blank=True)
    observacao_admissional = models.CharField(verbose_name="Obs Admissional", max_length=50, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    # Garantir que o funcionário não seja repetido para a mesma data de contratação
    class Meta:
        unique_together = ('nome_funcionario', 'data_contratacao')  # Um funcionário só pode ter uma contratação por data de pagamento


class Rescisao(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    data_desligamento = models.DateField(verbose_name="Dt Desligamento", null=False, blank=False)
    devolucao_uniforme = models.CharField(verbose_name="Devolução Uniforme", max_length=10, null=True, blank=True)
    data_exame_demissional = models.DateField(verbose_name="Dt Demissional", null=True, blank=True)
    data_homologacao = models.DateField(verbose_name="Dt Homologação", null=True, blank=True)
    tipo_desligamento = models.CharField(verbose_name="Forma Desligammento", max_length=30, null=False, blank=False)
    contabilidade_rescisao = models.CharField(verbose_name="Contabilidade Rescisão", max_length=10, null=True, blank=True)
    observacao_demissional = models.CharField(verbose_name="Obs Demissional", max_length=20, null=True, blank=True)
    status_rescisao = models.CharField(verbose_name="Status Rescisão", max_length=10, null=True, blank=True)
    # author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)


class Pagamento(models.Model):
    lista_tipo_pagamento = [
                            ('Salário', 'Salário'),
                            ('Adiantamento', 'Adiantamento'),
                            ('Vale', 'Vale'),
                            ('Vale Transporte', 'Vale Transporte'), 
                            ('Extra', 'Extra'),
                            ('Rescisão', 'Rescisão'),
                            ('Comissão', 'Comissão'),
                            ('Férias', 'Férias'),
                            ('13° Salário', '13° Salário')
                            ]
    lista_forma_pagamento = [
                             ('Conta Salário', 'Conta Salário'),
                             ('Dinheiro', 'Dinheiro'),
                             ('Transferência', 'Transferência'),
                             ('Pix', 'Pix'),
                             ('Cheque', 'Cheque'),
                             ('Multa Recisória', 'Multa Recisória')
                             ]
    created_at = models.DateTimeField(auto_now_add=True)
    # Chave estrangeira para Funcionario, associando a PK de nome
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    data_pagamento = models.DateField(verbose_name="Data Pagamento", null=False, blank=False,)
    valor_pago = models.DecimalField(verbose_name="Valor Pago", max_digits=9, decimal_places=2, null=False, blank=False)
    tipo_pagamento = models.CharField(verbose_name="Tipo de Pagamento", max_length=15, choices=lista_tipo_pagamento, null=False, blank=False)
    forma_pagamento = models.CharField(verbose_name="Forma de Pagamento", max_length=15, choices=lista_forma_pagamento, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=False)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)