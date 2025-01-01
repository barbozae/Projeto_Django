from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Fornecedor, Compras


class FornecedorListView(ListView):
    model = Fornecedor
    template_name = 'fornecedor_list.html'  # Garante que o template correto será usado


class FornecedorCreateView(CreateView):
    model = Fornecedor
    # campos que o usuario precisa preencher
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    # após o salvamentos redireciona para a view vendas
    success_url = reverse_lazy("fornecedor_list")


class FornecedorUpDateView(UpdateView):
    model = Fornecedor
    fields = ["nome_empresa", "cnpj", "nome_contato", "telefone", "email",
              "endereco", "cep", "numero", "bairro", "cidade"]
    success_url = reverse_lazy("fornecedor_list")


class ComprasListView(ListView):
    model = Compras
    

class ComprasCreateView(CreateView):
    model = Compras
    # campos que o usuario precisa preencher
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")


class ComprasUpDateView(UpdateView):
    model = Compras
    fields = ["data_compra", "data_vencimento", "data_pagamento", "fornecedor", "valor_compra", "valor_pago",
              "numero_boleto", "grupo_produto", "produto", "classificacao", "forma_pagamento", "observacao","qtd"]
    success_url = reverse_lazy("compras_list")


class ComprasDeleteView(DeleteView):
    model = Compras
    success_url = reverse_lazy("compras_list")