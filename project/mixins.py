from django.shortcuts import redirect


# Um mixin para filtrar os objetos pelo tenant associado ao usuário logado.
# class TenantQuerysetMixin:
#     def get_queryset(self):
#         tenant = getattr(self.request.user, 'tenant', None)
#         if not tenant:
#             return self.model.objects.none()  # Retorna uma queryset vazia se o tenant não for encontrado
#         return self.model.objects.filter(tenant=tenant)

# TODO ao buscar funcionario que não existe em cadastro o tenant se perde
from django.core.exceptions import PermissionDenied

class TenantQuerysetMixin:
    """
    Um mixin para filtrar os objetos pelo tenant associado ao usuário logado.
    """
    def get_queryset(self):
        # Obtém o tenant associado ao usuário logado
        tenant = getattr(self.request.user, 'tenant', None)
        

        # Se o tenant não for encontrado, usa o tenant do usuário logado
        if not tenant:
            tenant = self.request.user.tenant  # Garante que o tenant do usuário seja usado

        # Se o tenant não for encontrado, lança um erro ou toma uma ação padrão
        if not tenant:
            raise PermissionDenied("Tenant não encontrado para o usuário logado.")  # Lança um erro explícito
        
        # Filtra os objetos pelo tenant
        return self.model.objects.filter(tenant=tenant)

# caso usuário não tenha acesso conforme permissões consedidas seria direcionado para página Home
class HandleNoPermissionMixin:
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')  # Redireciona para a página de login
        return redirect('home')  # Redireciona para a home se o usuário não tiver permissão