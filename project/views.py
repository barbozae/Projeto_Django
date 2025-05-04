from django.shortcuts import render, redirect
from django.urls import reverse


def home_view(request):
    # Tenta obter o tenant do usuário autenticado, se disponível
    tenant = getattr(request.user, 'tenant', None)

    # Se o tenant não estiver associado ao usuário, tenta pegar da URL
    if not tenant:
        tenant = request.GET.get('tenant')

    # Se ainda assim o tenant não for encontrado, redireciona para o login
    if not tenant:
        return redirect(reverse('login'))

    # Formata o tenant (opcional, se necessário)
    tenant = str(tenant).lower().replace(' ', '_')

    # Renderiza a página home com o tenant no contexto
    return render(request, 'home.html', {'tenant': tenant})