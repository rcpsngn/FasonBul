from django.contrib import admin
from .models import AboutPage, Statistic


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_at")

    def has_add_permission(self, request):
        # Sadece 1 adet Hakkımızda kaydı oluşturulabilmesini sağlar
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "order")
    list_editable = ("value", "order")