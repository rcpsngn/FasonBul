from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'reviewee', 'contract', 'workmanship_score', 'timeliness_score', 'payment_discipline_score', 'defect_rate_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('reviewer__username', 'reviewee__username')
