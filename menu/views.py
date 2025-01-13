from django.shortcuts import render
from .models import Menu, Category


def menu_view(request):
    categories = Category.objects.filter(is_published=True)  # Recupera as categorias publicadas
    images = Menu.objects.filter(is_published=True, category__is_published=True)  # Itens do menu publicados e com categoria publicada
    carousel_images = Menu.objects.filter(carousel=True)  # Somente os itens para o carrossel
    return render(request, 'menu/menu.html', {'images': images, 'categories': categories, 'carousel_images': carousel_images})