from django.db import models
from django.contrib.auth.models import AbstractUser


class Tenant(models.Model):
    name = models.CharField(max_length=15, unique=True)
    domain = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT)
    phone = models.CharField(max_length=13, blank=True, null=True)
    birth_date = models.DateField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Modifique o related_name dos campos groups e user_permissions
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_set',  # Adicionando um nome diferente para evitar o conflito
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='custom_user_permissions_set',  # Adicionando um nome diferente para evitar o conflito
        blank=True
    )