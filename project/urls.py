from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from users.views import register

# def home(request):
#     return render(request, 'home.html')

# Função personalizada para logout
def custom_logout(request):
    logout(request)  # Encerra a sessão do usuário
    return redirect('/login/')  # Redireciona para a página de login

urlpatterns = [
                path('admin/', admin.site.urls),

                path('register/', register, name='register'),
                path('logout/', custom_logout, name='logout'),  # Substitui a LogoutView
                # path('', home, name='home'),  # Rota para a página inicial

                path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

                path('', include('vendas.urls')),
                path('', include('funcionarios.urls')),
                path('', include('compras.urls')),
            ]