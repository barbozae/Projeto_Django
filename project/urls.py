from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

# http://127.0.0.1:8000/admin/?tenant=modelo_1
# http://127.0.0.1:8000/?tenant=modelo_1

# Função personalizada para logout
def custom_logout(request):
    logout(request)  # Encerra a sessão do usuário
    return redirect('home')  # Redireciona para a página de login

urlpatterns = [
                path('admin/', admin.site.urls),

                path('', views.home_view, name='home'),

                path('', include('users.urls')),
                path('', include('vendas.urls')),
                path('', include('funcionarios.urls')),
                path('', include('compras.urls')),
                path('', include('menu.urls')),
                path('', include('financeiro.urls')),
            ]

# Servindo arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)