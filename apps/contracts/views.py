from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages

from apps.chat.models import Conversation
from .models import Contract
from .forms import ContractForm


def _get_conversation_or_404(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if not conversation.is_participant(request.user):
        raise Http404("Bu sohbete erişim yetkiniz yok.")
    return conversation


@login_required
def contract_edit_view(request, conversation_pk):
    conversation = _get_conversation_or_404(request, conversation_pk)
    contract = getattr(conversation, 'contract', None)

    if contract and contract.is_fully_approved:
        messages.info(request, 'Bu sözleşme her iki taraf tarafından da onaylanmış, artık düzenlenemez.')
        return redirect('contracts:contract_detail', conversation_pk=conversation_pk)

    if request.method == 'POST':
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            new_contract = form.save(commit=False)
            new_contract.conversation = conversation
            if not contract:
                new_contract.created_by = request.user
            else:
                new_contract.reset_approvals()
            new_contract.save()
            messages.success(request, 'Sözleşme kaydedildi. Şimdi karşı tarafın onayı bekleniyor.')
            return redirect('contracts:contract_detail', conversation_pk=conversation_pk)
    else:
        form = ContractForm(instance=contract)

    context = {
        'form': form,
        'conversation': conversation,
        'contract': contract,
    }
    return render(request, 'contracts/contract_form.html', context)


@login_required
def contract_detail_view(request, conversation_pk):
    conversation = _get_conversation_or_404(request, conversation_pk)
    contract = getattr(conversation, 'contract', None)
    if not contract:
        return redirect('contracts:contract_edit', conversation_pk=conversation_pk)

    context = {
        'conversation': conversation,
        'contract': contract,
    }
    return render(request, 'contracts/contract_detail.html', context)


@login_required
def contract_approve_view(request, conversation_pk):
    conversation = _get_conversation_or_404(request, conversation_pk)
    contract = get_object_or_404(Contract, conversation=conversation)
    contract.approve_for(request.user)
    return redirect('contracts:contract_detail', conversation_pk=conversation_pk)
