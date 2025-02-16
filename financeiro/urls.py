from django.urls import path
from . import views


urlpatterns = [
    path('dashboard_vendas', views.dashboard_vendas, name='dashboard_vendas'),
]
