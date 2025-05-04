from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Menu, Category, Tenant


@login_required
def menu_view(request):
    categories = Category.objects.filter(is_published=True)  # Recupera as categorias publicadas
    images = Menu.objects.filter(is_published=True, category__is_published=True)  # Itens do menu publicados e com categoria publicada
    carousel_images = Menu.objects.filter(carousel=True)  # Somente os itens para o carrossel
    return render(request, 'menu/menu.html', {'images': images, 'categories': categories, 'carousel_images': carousel_images})



# from django.shortcuts import get_object_or_404
# from users.models import Tenant  # Modelo de Tenant


# @login_required
# def menu_view(request):
#     # Obtém o parâmetro `tenant` da query string
#     tenant_name = request.GET.get('tenant')
#     if not tenant_name:
#         return render(request, '404.html', {'message': 'Tenant não encontrado'})  # Página 404 customizada

#     # Valida o tenant
#     tenant = get_object_or_404(Tenant, name=tenant_name)

#     # Filtra os dados com base no tenant
#     categories = Category.objects.filter(is_published=True, tenant=tenant)
#     images = Menu.objects.filter(
#         is_published=True,
#         category__is_published=True,
#         tenant=tenant
#     )
#     carousel_images = Menu.objects.filter(carousel=True, tenant=tenant)

#     # Renderiza o template com os dados filtrados
#     return render(
#         request,
#         'menu/menu.html',
#         {
#             'images': images,
#             'categories': categories,
#             'carousel_images': carousel_images,
#             'tenant': tenant
#         }
#     )


# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseNotFound
# from .models import Menu, Category
# from users.models import Tenant

# @login_required
# def menu_view(request):
#     try:
#         # Obtém o parâmetro tenant da query string
#         tenant_identifier = request.GET.get('tenant')
        
#         if not tenant_identifier:
#             return HttpResponseNotFound('Parâmetro tenant não fornecido na URL')
        
#         # Busca o tenant pelo domain (ou name, conforme sua necessidade)
#         tenant = get_object_or_404(Tenant, domain=tenant_identifier)
        
#         # Filtra os dados com base no tenant
#         categories = Category.objects.filter(is_published=True, tenant=tenant)
#         images = Menu.objects.filter(
#             is_published=True,
#             category__is_published=True,
#             tenant=tenant
#         )
#         carousel_images = Menu.objects.filter(carousel=True, tenant=tenant)
        
#         # Renderiza o template com os dados filtrados
#         return render(
#             request,
#             'menu/menu.html',
#             {
#                 'images': images,
#                 'categories': categories,
#                 'carousel_images': carousel_images,
#                 'tenant': tenant
#             }
#         )
    
#     except Exception as e:
#         # Log do erro para debug
#         import logging
#         logger = logging.getLogger(__name__)
#         logger.error(f"Erro em menu_view: {str(e)}")
        
#         return HttpResponseNotFound('Ocorreu um erro ao processar sua requisição')
