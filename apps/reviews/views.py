from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from apps.contracts.models import Contract
from .models import Review
from .forms import ReviewForm


@login_required
def review_create_view(request, contract_pk):
    contract = get_object_or_404(Contract, pk=contract_pk)

    if request.user not in (contract.owner, contract.bidder):
        raise Http404("Bu sözleşmeye erişim yetkiniz yok.")

    if not contract.is_completed:
        messages.warning(request, 'Değerlendirme yapabilmek için önce her iki tarafın da işi tamamlandı olarak işaretlemesi gerekir.')
        return redirect('contracts:contract_detail', conversation_pk=contract.conversation_id)

    reviewee = contract.bidder if request.user == contract.owner else contract.owner

    existing = Review.objects.filter(contract=contract, reviewer=request.user).first()
    if existing:
        messages.info(request, 'Bu iş için değerlendirmenizi zaten göndermiştiniz.')
        return redirect('accounts:public_profile', username=reviewee.username)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.contract = contract
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, 'Değerlendirmeniz için teşekkürler.')
            return redirect('accounts:public_profile', username=reviewee.username)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'contract': contract,
        'reviewee': reviewee,
    }
    return render(request, 'reviews/review_form.html', context)
