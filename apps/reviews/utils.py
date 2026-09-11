from apps.contracts.models import Contract


def get_pending_reviews(user):
    """Kullanıcının taraf olduğu, iş tamamlanmış ama kendisinin henüz değerlendirme
    yapmadığı sözleşmeleri döner. Roadmap kuralı: 'Puanlama yapılmadan yeni ilan
    açılması engellenmeli' - bu liste dolu olduğu sürece yeni ilan açılamaz."""
    contracts = Contract.objects.filter(owner_completed=True, bidder_completed=True).filter(
        conversation__proposal__advert__owner=user
    ) | Contract.objects.filter(owner_completed=True, bidder_completed=True).filter(
        conversation__proposal__bidder=user
    )
    contracts = contracts.distinct().exclude(reviews__reviewer=user)
    return contracts
