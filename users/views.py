from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .models import Tenant
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView


def register(request):
    # Verifica se o tenant foi passado pela URL
    tenant_name = request.GET.get('tenant')  # Pega o parâmetro 'tenant' da URL
    tenant = None
    
    if tenant_name:
        try:
            tenant = Tenant.objects.get(domain=tenant_name)  # Busca o tenant pelo domínio
        except Tenant.DoesNotExist:
            messages.error(request, 'Tenant não encontrado.')
            return redirect('home')  # Redireciona caso o tenant não exista

    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado.')
        return redirect(f"{reverse('home')}?tenant={tenant_name}")

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Cria o usuário mas não salva no banco ainda
            user = form.save(commit=False)

            # Verifica e associa o tenant
            if tenant:
                user.tenant = tenant
                user.save()  # Agora salva no banco com o tenant associado

                messages.success(request, 'Usuário criado com sucesso!')
                return redirect(f"{reverse('login')}?tenant={tenant_name}")
            else:
                messages.error(request, 'Erro ao associar tenant ao usuário.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form, 'tenant': tenant_name})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        tenant = request.GET.get('tenant')
        return super().get(request, *args, **kwargs)
    
    def get_success_url(self):
        tenant = self.request.GET.get('tenant') or self.request.POST.get('tenant')
        if tenant:
            url = f'{reverse_lazy("menu")}?tenant={tenant}'
            return url
        return super().get_success_url()


class CustomLogoutView(LogoutView):
    template_name = 'users/logout.html'

    def get_next_page(self):
        # Captura o tenant da URL (GET)
        tenant = self.request.GET.get('tenant')

        if tenant:
            # Adiciona o tenant à URL de redirecionamento
            url = f'{reverse_lazy("login")}?tenant={tenant}'
            return url
        else:
            # Redireciona para o login sem tenant
            return reverse_lazy("login")
        
