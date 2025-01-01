from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

# from .forms import ContratacaoForm
from .models import Cadastro, Contratacao, Pagamento, Rescisao
# from .forms import ContratacaoForm


class CadastroListView(ListView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_list.html'  # Garante que o template correto será usado
    context_object_name = 'funcionarios_list'


class CadastroCreateView(CreateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    # campos que o usuario precisa preencher
    fields = ["nome_funcionario", "rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")


class CadastroUpDateView(UpdateView):
    model = Cadastro
    template_name = 'funcionarios/funcionarios_form.html'  # Força o uso do template correto
    fields = ["rg", "cpf", "carteira_trabalho", "cidade",
              "bairro", "endereco", "numero", "telefone", "banco", "agencia", "conta"]
    success_url = reverse_lazy("funcionarios_list")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['funcionario'] = self.object  # Passa o objeto como 'funcionario'
        return context


class ContratacaoListView(ListView):
    model = Contratacao
    template_name = 'funcionarios/contratacao_list.html'  # Garante que o template correto será usado


class ContratacaoCreateView(CreateView):
    model = Contratacao
    fields = ["nome_funcionario", "cargo", "setor", "data_exame_admissional", "data_contratacao", "salario",
                  "documentacao_admissional", "contabilidade_admissional", "status_admissional", "observacao_admissional"]
    success_url = reverse_lazy("contratacao_list")


class ContratacaoUpDateView(UpdateView):
    model = Contratacao
    fields = ["nome_funcionario", "cargo", "setor", "data_exame_admissional", "data_contratacao", "salario",
              "documentacao_admissional", "contabilidade_admissional", "status_admissional", "observacao_admissional"]
    # form_class = ContratacaoCreateView
    success_url = reverse_lazy("contratacao_list")


class PagamentoListView(ListView):
    model = Pagamento
    template_name = 'funcionarios/pagamento_list.html'


class PagamentoCreateView(CreateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")


class PagamentoUpDateView(UpdateView):
    model = Pagamento
    fields = ["nome_funcionario", "data_pagamento", "valor_pago", "tipo_pagamento", "forma_pagamento"]
    success_url = reverse_lazy("pagamento_list")


class RescisaoListView(ListView):
    model = Rescisao
    template_name = 'funcionarios/rescisao_list.html'


class RescisaoCreateView(CreateView):
    model = Rescisao
    fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              "status_rescisao"]
    success_url = reverse_lazy("rescisao_list")


class RescisaoUpDateView(UpdateView):
    model = Rescisao
    fields = ["nome_funcionario", "data_desligamento", "devolucao_uniforme", "data_exame_demissional",
              "data_homologacao", "tipo_desligamento", "contabilidade_rescisao", "observacao_demissional",
              "status_rescisao"]
    success_url = reverse_lazy("rescisao_list")