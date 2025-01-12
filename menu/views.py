from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Menu
from django.shortcuts import render


def menu_view(request):
    images = Menu.objects.filter(is_published=True, category__is_published=True) # Busca apenas imagens is_published igual a True em Menu e Category
    return render(request, 'menu/menu.html', {'images': images})