from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Q

from .models import Conversation
from .forms import MessageForm


def _get_conversation_or_404(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if not conversation.is_participant(request.user):
        raise Http404("Bu sohbete erişim yetkiniz yok.")
    return conversation


@login_required
def inbox_view(request):
    conversations = list(
        Conversation.objects.filter(
            Q(proposal__advert__owner=request.user) | Q(proposal__bidder=request.user)
        ).select_related('proposal', 'proposal__advert', 'proposal__bidder', 'proposal__advert__owner')
    )
    # Şablonda argümanlı metot çağrısı yapılamadığı için karşı tarafı burada hesaplıyoruz
    for conv in conversations:
        conv.other_user = conv.other_participant(request.user)

    context = {'conversations': conversations}
    return render(request, 'chat/inbox.html', context)


@login_required
def conversation_detail_view(request, pk):
    conversation = _get_conversation_or_404(request, pk)
    other_user = conversation.other_participant(request.user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('chat:conversation_detail', pk=pk)
    else:
        form = MessageForm()

    # Karşı tarafın gönderdiği okunmamış mesajları okundu olarak işaretle
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    context = {
        'conversation': conversation,
        'other_user': other_user,
        'thread': conversation.messages.select_related('sender').all(),
        'form': form,
    }
    return render(request, 'chat/conversation_detail.html', context)


@login_required
def confirm_meeting_view(request, pk):
    conversation = _get_conversation_or_404(request, pk)
    conversation.confirm_meeting_for(request.user)
    return redirect('chat:conversation_detail', pk=pk)
