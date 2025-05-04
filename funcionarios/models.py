from django.conf import settings
from django.db import models
from users.models import Tenant
from django.core.exceptions import ValidationError


class Cadastro(models.Model):
    LIST_BANK = [('Banco do Brasil', 'Banco do Brasil'),
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
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.CharField(verbose_name="Funcionário", max_length=40 , blank=False, unique=True)
    rg = models.CharField(verbose_name="RG", max_length=14, null=True , blank=True)
    cpf = models.CharField(verbose_name="CPF", max_length=14, null=True , blank=True)
    carteira_trabalho = models.CharField(verbose_name="CTPS", max_length=12, null=True, blank=True)
    endereco = models.CharField(verbose_name="Endereço", max_length=40, null=True, blank=True)
    numero = models.CharField(verbose_name="Número", max_length=255, null=True, blank=True)
    bairro = models.CharField(verbose_name="Bairro", max_length=20, null=True, blank=True)
    cidade = models.CharField(verbose_name="Cidade", max_length=30, null=True, blank=True)
    telefone = models.CharField(verbose_name="Telefone", max_length=13, null=True, blank=True)
    banco = models.CharField(verbose_name="Banco", choices=LIST_BANK, max_length=15, null=True, blank=True)
    agencia = models.CharField(verbose_name="Agencia", max_length=7, null=True, blank=True)
    conta = models.CharField(verbose_name="Conta", max_length=10, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        # Retorna uma string representando o funcionário devido a ForeignKey em PG_Funcionarios
        return f"{self.nome_funcionario}"


class Contratacao(models.Model):
    CARGOS_POR_SETOR = {
                    'Administração': ["Gerente Financeiro", "Auxiliar Adm"],
                    'Cozinha': ["Chef", "Cozinheiro", "Cozinheiro Auxiliar"],
                    'Limpeza': ["Faxineira(o)"],
                    'Sushi': ["Peixeiro", "Sushiman", "Sushiman Auxiliar"],
                    'Salão': ["Caixa", "Cumin", "Garçom", "Gerente Geral", "Maitre", "Recepcionista"],
                    'Bar': ["Barman", "Copeiro"],
                    'Vallet': ["Manobrista"]
                    }
    
    SETOR_CHOICES = [(key, key) for key in CARGOS_POR_SETOR.keys()]
    CARGO_CHOICES = [(value, value) for sublist in CARGOS_POR_SETOR.values() for value in sublist]

    DOC_CONTABILIDADE = [('Enviado', 'Enviado'),
                         ('Não Enviado', 'Não Enviado')]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    setor = models.CharField(verbose_name="Setor", choices=SETOR_CHOICES, max_length=13, null=False, blank=False)
    cargo = models.CharField(verbose_name="Cargo", choices=CARGO_CHOICES, max_length=19, null=False, blank=False)
    data_exame_admissional = models.DateField(verbose_name="Dt Exame Admissional", null=True, blank=True)
    data_contratacao = models.DateField(verbose_name="Data Contratação", null=False, blank=False)
    salario = models.DecimalField(verbose_name="Salário", max_digits=9, decimal_places=2, null=True, blank=True)
    contabilidade_admissional = models.CharField(verbose_name="Doc Contabilidade", choices=DOC_CONTABILIDADE, max_length=11, null=True, blank=True)
    status_admissional = models.BooleanField(verbose_name="Status Rescisão", default=False)
    observacao_admissional = models.CharField(verbose_name="Obs Admissional", max_length=50, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    # Garantir que o funcionário não seja repetido para a mesma data de contratação
    class Meta:
        unique_together = ('nome_funcionario', 'data_contratacao')  # Um funcionário só pode ter uma contratação por data de pagamento

    @property
    def status_rescisao(self):
        """
        Verifica se há uma rescisão associada a esta contratação. 
        Estou usando status_rescisao em contratacao_list.html para ver se o funcionario esta ativo
        """
        return Rescisao.objects.filter(nome_funcionario_id=self.nome_funcionario_id).exists()

    def save(self, *args, **kwargs):
        # Lógica para determinar o status_admissional
        if (
            self.contabilidade_admissional == 'Enviado' and  # A coluna contabilidade_admissional deve ter o valor 'True'
            self.data_contratacao, self.data_exame_admissional is not None  # datas devem serem preenchidas
        ):
            self.status_admissional = True
        else:
            self.status_admissional = False

        super(Contratacao, self).save(*args, **kwargs)  # Chama o método save origina

    def __str__(self):
        # Retorna uma string representando o funcionário devido a ForeignKey em PG_Funcionarios
        return f"{self.nome_funcionario}"


class Rescisao(models.Model):
    LIST_CHOICES = [('Dispensa sem justa causa', 'Dispensa sem justa causa'),
                     ('Demissão por justa causa', 'Demissão por justa causa'),
                     ('Pedido de demissão','Pedido de demissão'),
                     ('Término do contrato', 'Término do contrato'),
                     ('Rescisão indireta', 'Rescisão indireta'),
                     ('Rescisão por culpa recíproca', 'Rescisão por culpa recíproca')
                     ]
    UNIFORME = [('Entregue', 'Entregue'),
                  ('Não Entregue', 'Não Entregue')
                  ]
    DOC_CONTABILIDADE = [('Enviado', 'Enviado'),
                         ('Não Enviado', 'Não Enviado')]
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    data_desligamento = models.DateField(verbose_name="Data Desligamento", null=False, blank=False)
    devolucao_uniforme = models.CharField(verbose_name="Devolução Uniforme", choices=UNIFORME, max_length=12, null=True, blank=True)
    data_exame_demissional = models.DateField(verbose_name="Data Exame Demissional", null=True, blank=True)
    data_homologacao = models.DateField(verbose_name="Data Homologação", null=True, blank=True)
    tipo_desligamento = models.CharField(verbose_name="Forma Desligamento", choices=LIST_CHOICES, max_length=30, null=False, blank=False)
    contabilidade_rescisao = models.CharField(verbose_name="Contabilidade Documentação", choices=DOC_CONTABILIDADE, max_length=11, null=True, blank=True)
    observacao_demissional = models.CharField(verbose_name="Observação", max_length=40, null=True, blank=True)
    status_rescisao = models.BooleanField(verbose_name="Status Rescisão", default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    # Garantir que o funcionário não seja repetido para a mesma data de contratação
    class Meta:
        unique_together = ('nome_funcionario', 'data_desligamento')  # Um funcionário só pode ter uma contratação por data de pagamento


    def save(self, *args, **kwargs):
        # Lógica para determinar o status_rescisao
        if (
            self.devolucao_uniforme == 'Entregue' and  # A coluna devolucao_uniforme deve ter o valor 'True'
            self.data_exame_demissional is not None and  # data_exame_demissional deve ser preenchida
            self.contabilidade_rescisao == 'Enviado'  # A coluna contabilidade_rescisao deve ter o valor 'True'
        ):
            self.status_rescisao = True
        else:
            self.status_rescisao = False

        super(Rescisao, self).save(*args, **kwargs)  # Chama o método save origina


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
    
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # Chave estrangeira para Funcionario, associando a PK de nome
    nome_funcionario = models.ForeignKey(Cadastro, on_delete=models.PROTECT, verbose_name="Funcionário", null=False)
    data_pagamento = models.DateField(verbose_name="Data Pagamento", null=False, blank=False,)
    valor_pago = models.DecimalField(verbose_name="Valor Pago", max_digits=9, decimal_places=2, null=False, blank=False)
    tipo_pagamento = models.CharField(verbose_name="Tipo de Pagamento", max_length=15, choices=lista_tipo_pagamento, null=False, blank=False)
    forma_pagamento = models.CharField(verbose_name="Forma de Pagamento", max_length=15, choices=lista_forma_pagamento, null=False, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=False, default=1)
    dt_atualizado = models.DateTimeField(auto_now=True, null=False, blank=False)

    # as duas funções abaixo é para EVITAR que funcionarios desligado recebam pagamentos e edições
    def clean(self):
        # Verifica se o funcionário tem uma rescisão
        if Rescisao.objects.filter(nome_funcionario=self.nome_funcionario).exists():
            raise ValidationError(f'O funcionário {self.nome_funcionario} foi desligado e não pode receber pagamentos.')
        super().clean()

    def save(self, *args, **kwargs):
        # Chama o método clean para garantir que a validação seja executada
        self.clean()
        super(Pagamento, self).save(*args, **kwargs)