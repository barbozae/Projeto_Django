def tenant_context(request):
    return {
        'tenant': request.GET.get('tenant', None),
    }
