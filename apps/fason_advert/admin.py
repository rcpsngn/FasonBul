from django.contrib import admin
from .models import AdvertCategory, Advert, Proposal, ProposalOffer


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


class ProposalOfferInline(admin.TabularInline):
    model = ProposalOffer
    extra = 0
    raw_id_fields = ("sender",)


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("advert", "bidder", "status", "latest_price_offer", "latest_quantity_offer", "created_at", "responded_at")
    list_filter = ("status",)
    search_fields = ("advert__title", "bidder__username")
    raw_id_fields = ("advert", "bidder", "awaiting_response_from")
    inlines = [ProposalOfferInline]

    @admin.display(description="Birim Fiyat (TL)")
    def latest_price_offer(self, obj):
        offer = obj.latest_offer
        return offer.price_offer if offer else "-"

    @admin.display(description="Adet")
    def latest_quantity_offer(self, obj):
        offer = obj.latest_offer
        return offer.quantity_offer if offer else "-"