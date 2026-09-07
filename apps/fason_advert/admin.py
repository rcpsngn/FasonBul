from django.contrib import admin
from .models import AdvertCategory, Advert


@admin.register(AdvertCategory)
class AdvertCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "advert_type", "owner", "city", "is_active", "created_at")
    list_filter = ("is_active", "advert_type", "category", "city", "created_at")
    search_fields = ("title", "description", "city", "district")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("owner",)