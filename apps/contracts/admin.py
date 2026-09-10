from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'quantity', 'unit_price', 'due_date', 'owner_approved', 'bidder_approved', 'approved_at')
    list_filter = ('owner_approved', 'bidder_approved')
    readonly_fields = ('approved_at',)
