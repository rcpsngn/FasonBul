from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, Document, Machine, DocumentAccessRequest


class MachineInline(admin.TabularInline):
    model = Machine
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active", "city")
    search_fields = ("username", "email", "first_name", "last_name", "profile__company_name")

    fieldsets = UserAdmin.fieldsets + (
        ('Ek Bilgiler', {'fields': ('role', 'phone', 'city', 'avatar')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Ek Bilgiler', {'fields': ('role', 'email', 'phone', 'city')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "is_verified", "verified_at")
    list_filter = ("is_verified",)
    search_fields = ("user__username", "company_name", "tax_number")
    readonly_fields = ("is_verified", "verified_at")
    inlines = [MachineInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("user", "document_type", "uploaded_at")
    list_filter = ("document_type",)
    search_fields = ("user__username",)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("profile", "name", "quantity")
    search_fields = ("name", "profile__company_name")


@admin.register(DocumentAccessRequest)
class DocumentAccessRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "document", "status", "requested_at", "responded_at")
    list_filter = ("status",)
    search_fields = ("requester__username", "document__user__username")
