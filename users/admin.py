from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Tenant, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Customize se necessário, ou mantenha o padrão
    fieldsets = UserAdmin.fieldsets + (  # Adiciona novos campos ao admin
        ('Informações adicionais', {
            'fields': ('tenant', 'phone'),
        }),
    )
    list_display = ['username', 'email', 'tenant', 'is_staff', 'is_active']
    list_filter = ['tenant', 'is_staff', 'is_active']


# Registro padrão para o modelo Tenant
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain']
    search_fields = ['name', 'domain']
