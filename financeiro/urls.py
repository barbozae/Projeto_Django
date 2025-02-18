from django.urls import path
from . import views


urlpatterns = [
    path('dashboard_vendas', views.dashboard_vendas, name='dashboard_vendas'),
    path('dashboard_compras', views.dashboard_compras, name='dashboard_compras'),
    path('dashboard_funcionarios', views.dashboard_funcionarios, name='dashboard_funcionarios'),
]
