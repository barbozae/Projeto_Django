from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Cria o novo usuário com os dados do formulário
            return redirect('login')  # Redireciona para a tela de login
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})
