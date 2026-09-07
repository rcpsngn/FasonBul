from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "order", "is_active", "created_at")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}