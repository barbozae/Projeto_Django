from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()  # Obtém o modelo de usuário customizado

# Formulário de criação de usuário com a customização do campo tenant
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Primeiro Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Último Nome')
    birth_date = forms.DateField(required=True, label='Data de Nascimento', widget=forms.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True, label='E-mail')
    phone = forms.CharField(max_length=13, required=False, label='Telefone')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birth_date', 'email', 'phone', 'password1', 'password2']
        help_texts = {
            'username': None,  # Remove a mensagem de ajuda para o campo "username"
        }