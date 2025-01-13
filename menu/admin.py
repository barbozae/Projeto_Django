from django.contrib import admin

from .models import Category, Menu


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "is_published", "cover", "carousel")
    search_fields = ("title",)