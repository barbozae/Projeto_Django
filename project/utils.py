from urllib.parse import quote
from django.urls import reverse_lazy

def generate_success_url(view_name, tenant):
    """
    Gera uma URL de sucesso com o parâmetro 'tenant'.
    Isso é útil para redirecionar o usuário para a página correta após criar, atualizar ou excluir um objeto
    """
    # formatando o tenant para minúsculas e substituindo espaços por underscores
    if tenant:
        tenant = str(tenant).lower().replace(' ', '_')  # Converte para minúsculas e substitui espaços por underscores
    tenant_encoded = quote(tenant)  # Codifica o tenant corretamente
    return f"{reverse_lazy(view_name)}?tenant={tenant_encoded}"