from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Formulário personalizado de registro de usuário
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Primeiro Nome')
    last_name = forms.CharField(max_length=30, required=True, label='Último Nome')
    email = forms.EmailField(required=True, label='E-mail')


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,  # Remove a mensagem de ajuda para o campo "username"
        }