from django.http import Http404
from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ignorar caminhos de login e logout
        if request.path.startswith('/login/') or request.path.startswith('/logout/'):
            return self.get_response(request)

        # Ignorar restrição de tenant para superusuários
        if request.user.is_authenticated and request.user.is_superuser:
            request.tenant = None
            return self.get_response(request)

        # Processar o tenant para outros usuários
        dominio_atual = request.get_host().split(':')[0]
        tenant_param = request.GET.get('tenant', None)

        try:
            if tenant_param:
                request.tenant = Tenant.objects.get(domain=tenant_param)
            else:
                request.tenant = Tenant.objects.get(domain=dominio_atual)
        except Tenant.DoesNotExist:
            raise Http404("Tenant não encontrado.")
        
        return self.get_response(request)