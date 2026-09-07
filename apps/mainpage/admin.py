from django.contrib import admin
from .models import Banner, Statistic


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "subtitle")


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "order", "is_active")
    list_editable = ("order", "is_active")