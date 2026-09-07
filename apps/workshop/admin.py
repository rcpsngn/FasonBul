from django.contrib import admin
from .models import Workshop


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'district', 'phone', 'capacity', 'created_at')
    list_filter = ('category', 'city')
    search_fields = ('title', 'phone', 'city', 'district', 'address')
    ordering = ('-created_at',)

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('owner', 'title', 'category', 'phone', 'capacity')
        }),
        ('Konum Bilgileri', {
            'fields': ('city', 'district', 'address', 'latitude', 'longitude')
        }),
    )