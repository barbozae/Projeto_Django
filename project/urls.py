from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
                path('', include('menu.urls')),
            ]

# Servindo arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)