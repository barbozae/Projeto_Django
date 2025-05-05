from django.apps import AppConfig


class FinanceiroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financeiro'


# Incluindo o código para definir permissões personalizadas no app financeiro
class FinanceiroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'financeiro'

    def ready(self):
        # Definir permissões personalizadas
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        # Criar um ContentType fictício para o app financeiro
        content_type, created = ContentType.objects.get_or_create(app_label='financeiro', model='financeiro')

        # Criar permissões personalizadas
        Permission.objects.get_or_create(codename='view_dashboard_financeiro', name='Can view financeiro dashboard', content_type=content_type)
        Permission.objects.get_or_create(codename='edit_dashboard_financeiro', name='Can edit financeiro dashboard', content_type=content_type)