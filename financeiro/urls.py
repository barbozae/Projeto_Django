from django.urls import path
from .views import DashboardVendasView, DashboardComprasView, DashboardFuncionariosView, DashboardResumoView


urlpatterns = [
    path('dashboard_vendas', DashboardVendasView.as_view(), name='dashboard_vendas'),
    path('dashboard_compras', DashboardComprasView.as_view(), name='dashboard_compras'),
    path('dashboard_funcionarios', DashboardFuncionariosView.as_view(), name='dashboard_funcionarios'),
    path('dashboard_resumo', DashboardResumoView.as_view(), name='dashboard_resumo'),
]
