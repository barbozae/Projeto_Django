from django.urls import path
from vendas.views import VendasListView, VendasCreateView, VendasUpDateView, VendasDeleteView, vendas_resumo


urlpatterns = [
                # Rotas para vendas
                path('sales/', VendasListView.as_view(), name="venda_list"),
                path('create_vendas/', VendasCreateView.as_view(), name="create_vendas"),
                path('update_vendas/<int:pk>', VendasUpDateView.as_view(), name="update_vendas"),
                path('delete_vendas/<int:pk>', VendasDeleteView.as_view(), name="delete_vendas"),
                path('resume_vendas/', vendas_resumo, name="resume_vendas"),
]