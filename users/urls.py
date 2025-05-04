from django.urls import path, reverse
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, CustomPasswordChangeView, register
from django.contrib.auth import logout
from django.shortcuts import redirect


def simple_logout(request):
    tenant = request.GET.get('tenant')  # Captura o parâmetro 'tenant' da URL
    logout(request)  # Executa o logout do usuário
    if tenant:
        return redirect(f"{reverse('login')}?tenant={tenant}")  # Redireciona com o tenant
    return redirect('login')  # Redireciona sem tenant, se não estiver presente

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', simple_logout, name='logout'),
    path(
        'password_change/', 
        #  auth_views.PasswordChangeView.as_view(
        CustomPasswordChangeView.as_view(
             template_name='users/password_change.html', 
             success_url='/password_change_done/'
             ),
             name='password_change'),
    path(
        'password_change_done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
            ),
            name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]