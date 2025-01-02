from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views


# Função personalizada para logout
def custom_logout(request):
    logout(request)  # Encerra a sessão do usuário
    return redirect('/login/')  # Redireciona para a página de login

urlpatterns = [
                path('admin/', admin.site.urls),

                path('', views.home_view, name='home'),

                path('logout/', custom_logout, name='logout'),

                path('', include('users.urls')),
                path('', include('vendas.urls')),
                path('', include('funcionarios.urls')),
                path('', include('compras.urls')),
            ]