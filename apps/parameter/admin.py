from django.contrib import admin
from .models import SiteSetting, City, District, WorkType


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("title", "footer_text")

    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name",)
    inlines = [DistrictInline]


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    list_editable = ("is_active",)
    search_fields = ("name",)