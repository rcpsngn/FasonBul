from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Advert, AdvertCategory, Proposal
from .forms import AdvertForm, ProposalForm
from apps.reviews.utils import get_pending_reviews


def advert_list(request):
    categories = AdvertCategory.objects.all()
    adverts = Advert.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    advert_type = request.GET.get('type')
    city = request.GET.get('city')

    if category_slug:
        adverts = adverts.filter(category__slug=category_slug)
    if advert_type:
        adverts = adverts.filter(advert_type=advert_type)
    if city:
        adverts = adverts.filter(city__icontains=city)

    context = {
        'categories': categories,
        'adverts': adverts,
    }
    return render(request, 'fason_advert/list.html', context)


def advert_detail(request, slug):
    advert = get_object_or_404(Advert, slug=slug, is_active=True)
    related_adverts = Advert.objects.filter(category=advert.category, is_active=True).exclude(id=advert.id)[:3]

    is_owner = request.user.is_authenticated and request.user == advert.owner
    my_proposal = None
    proposal_form = None

    if request.user.is_authenticated and not is_owner:
        my_proposal = Proposal.objects.filter(advert=advert, bidder=request.user).first()
        if my_proposal is None or my_proposal.status == Proposal.Status.REJECTED:
            proposal_form = ProposalForm()

    context = {
        'advert': advert,
        'related_adverts': related_adverts,
        'is_owner': is_owner,
        'my_proposal': my_proposal,
        'proposal_form': proposal_form,
    }
    return render(request, 'fason_advert/detail.html', context)


@login_required
def advert_create(request):
    pending_reviews = get_pending_reviews(request.user)
    if pending_reviews.exists():
        messages.warning(
            request,
            'Yeni ilan açmadan önce tamamlanmış işleriniz için değerlendirme yapmanız gerekiyor.'
        )
        return redirect('contracts:contract_detail', conversation_pk=pending_reviews.first().conversation_id)

    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.owner = request.user
            advert.save()
            messages.success(request, 'İlanınız başarıyla oluşturuldu.')
            return redirect('fason_advert:detail', slug=advert.slug)
    else:
        form = AdvertForm()

    return render(request, 'fason_advert/form.html', {'form': form, 'title': 'Yeni İlan Oluştur'})


@login_required
def proposal_create_view(request, slug):
    advert = get_object_or_404(Advert, slug=slug, is_active=True)

    if advert.owner == request.user:
        messages.error(request, 'Kendi ilanınıza teklif veremezsiniz.')
        return redirect('fason_advert:detail', slug=slug)

    existing = Proposal.objects.filter(advert=advert, bidder=request.user).first()
    if existing and existing.status != Proposal.Status.REJECTED:
        messages.info(request, 'Bu ilana zaten bir teklif gönderdiniz.')
        return redirect('fason_advert:detail', slug=slug)

    if request.method == 'POST':
        form = ProposalForm(request.POST)
        if form.is_valid():
            if existing:
                proposal = existing
                proposal.status = Proposal.Status.PENDING
                proposal.responded_at = None
                proposal.awaiting_response_from = advert.owner
                proposal.save()
            else:
                proposal = Proposal.objects.create(
                    advert=advert,
                    bidder=request.user,
                    status=Proposal.Status.PENDING,
                    awaiting_response_from=advert.owner,
                )

            offer = form.save(commit=False)
            offer.proposal = proposal
            offer.sender = request.user
            offer.save()
            messages.success(request, 'Teklifiniz gönderildi.')
        else:
            messages.error(request, 'Teklif gönderilirken bir hata oluştu, lütfen tekrar deneyin.')

    return redirect('fason_advert:detail', slug=slug)


@login_required
def proposal_withdraw_view(request, pk):
    proposal = get_object_or_404(Proposal, pk=pk, bidder=request.user)
    advert_slug = proposal.advert.slug
    proposal.delete()
    messages.info(request, 'Teklifiniz geri çekildi.')
    return redirect('fason_advert:detail', slug=advert_slug)


@login_required
def advert_proposals_view(request, slug):
    """İlan sahibinin, ilanına gelen teklifleri görebileceği sayfa."""
    advert = get_object_or_404(Advert, slug=slug, owner=request.user)
    proposals = advert.proposals.select_related('bidder', 'bidder__profile').all()

    context = {
        'advert': advert,
        'proposals': proposals,
    }
    return render(request, 'fason_advert/advert_proposals.html', context)


@login_required
def my_proposals_view(request):
    """Kullanıcının gönderdiği tüm teklifler."""
    proposals = Proposal.objects.filter(bidder=request.user).select_related('advert', 'advert__owner')
    context = {'proposals': proposals}
    return render(request, 'fason_advert/my_proposals.html', context)


@login_required
def proposal_respond_view(request, pk, action):
    """action: 'accept' ya da 'reject'. Sadece ilan sahibi yanıt verebilir."""
    proposal = get_object_or_404(Proposal, pk=pk, advert__owner=request.user)

    if action == 'accept':
        proposal.status = Proposal.Status.ACCEPTED
        messages.success(request, f'{proposal.bidder} kullanıcısının teklifi kabul edildi.')
    else:
        proposal.status = Proposal.Status.REJECTED
        messages.info(request, f'{proposal.bidder} kullanıcısının teklifi reddedildi.')

    proposal.responded_at = timezone.now()
    proposal.save(update_fields=['status', 'responded_at'])
    return redirect('fason_advert:advert_proposals', slug=proposal.advert.slug)
