from django.db import models
from django.conf import settings
from users.models import Tenant


class Category(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=65)
    description = models.TextField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Menu(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    carousel = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='menu/covers/%Y/%m/%d/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    update_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    def __str__(self):
        return self.title