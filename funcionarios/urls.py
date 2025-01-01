from django.urls import path
from funcionarios.views import CadastroListView, CadastroCreateView, CadastroUpDateView, ContratacaoListView, ContratacaoCreateView, ContratacaoUpDateView, PagamentoListView, PagamentoCreateView, PagamentoUpDateView, RescisaoListView, RescisaoCreateView, RescisaoUpDateView

urlpatterns = [
                # Rotas para Funcionários
                path('funcionario/', CadastroListView.as_view(), name="funcionarios_list"),
                path('create_funcionarios/', CadastroCreateView.as_view(), name="create_funcionarios"),
                path('update_funcionarios/<int:pk>', CadastroUpDateView.as_view(), name="update_funcionarios"),

                # Rotas para contratação de funcionarios
                path('contratacao/', ContratacaoListView.as_view(), name="contratacao_list"),
                path('create_contratacao/', ContratacaoCreateView.as_view(), name="create_contratacao"),
                path('update_contratacao/<int:pk>', ContratacaoUpDateView.as_view(), name="update_contratacao"),

                # Rotas para pagamento de funcionarios
                path('payment/', PagamentoListView.as_view(), name="pagamento_list"),
                path('create_payment/', PagamentoCreateView.as_view(), name="create_payment"),
                path('update_payment/<int:pk>', PagamentoUpDateView.as_view(), name="update_payment"),

                # Rotas para rescisao de funcionarios
                path('rescisao/', RescisaoListView.as_view(), name="rescisao_list"),
                path('create_rescisao/', RescisaoCreateView.as_view(), name="create_rescisao"),
                path('update_rescisao/<int:pk>', RescisaoUpDateView.as_view(), name="update_rescisao"),
            ]