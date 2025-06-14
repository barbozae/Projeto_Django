from django.urls import path
from .views import DashboardVendasView, DashboardComprasView, DashboardFuncionariosView, DashboardResumoView, TaxaListView, TaxaCreateView,TaxaUpDateView


urlpatterns = [
    path('dashboard_vendas', DashboardVendasView.as_view(), name='dashboard_vendas'),
    path('dashboard_compras', DashboardComprasView.as_view(), name='dashboard_compras'),
    path('dashboard_funcionarios', DashboardFuncionariosView.as_view(), name='dashboard_funcionarios'),
    path('dashboard_resumo', DashboardResumoView.as_view(), name='dashboard_resumo'),

    path('taxas_vendas/', TaxaListView.as_view(), name='taxas_vendas'),
    path('create_taxas_vendas/', TaxaCreateView.as_view(), name="create_taxas_vendas"),
    path('update_taxas_vendas/<int:pk>', TaxaUpDateView.as_view(), name="update_taxas_vendas"),
]
