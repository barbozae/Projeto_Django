from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Ou o modelo customizado de usuário que você está usando
from .forms import CustomUserCreationForm
from django.contrib import messages  # Para exibir mensagens de erro/sucesso


def register(request):
    # Redireciona usuários autenticados
    if request.user.is_authenticated:
        messages.warning(request, 'Você já está logado e não pode criar uma nova conta.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Obtém o email do formulário
            if User.objects.filter(email=email).exists():
                # Exibe mensagem de erro se o email já existe
                messages.error(request, 'Este email já está em uso. Por favor, escolha outro.')
            else:
                form.save()  # Cria o novo usuário com os dados do formulário
                messages.success(request, 'Usuário criado com sucesso! Agora você pode fazer login.')
                return redirect('login')  # Redireciona para a tela de login
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})