from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .forms import (
    CustomUserCreationForm,
    ProfileUpdateForm,
    CompanyProfileForm,
    DocumentUploadForm,
    MachineForm,
)
from .models import User, Profile, Document, Machine, DocumentAccessRequest


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Aramıza hoş geldiniz! Hesabınız başarıyla oluşturuldu.')
            return redirect('accounts:profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Hoş geldiniz, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'accounts:profile')
            return redirect(next_url)
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Oturumunuz kapatıldı.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        company_form = CompanyProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and company_form.is_valid():
            user_form.save()
            company_form.save()
            messages.success(request, 'Profil bilgileriniz güncellendi.')
            return redirect('accounts:profile')
    else:
        user_form = ProfileUpdateForm(instance=request.user)
        company_form = CompanyProfileForm(instance=profile)

    pending_requests = DocumentAccessRequest.objects.filter(
        document__user=request.user,
        status=DocumentAccessRequest.Status.PENDING,
    ).select_related('requester', 'document')

    context = {
        'user_form': user_form,
        'company_form': company_form,
        'profile': profile,
        'documents': request.user.documents.all(),
        'machines': profile.machines.all(),
        'document_form': DocumentUploadForm(),
        'machine_form': MachineForm(),
        'pending_requests': pending_requests,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def public_profile_view(request, username):
    """Başka bir kullanıcının profilini salt-okunur gösterir. Belgeler doğrudan
    görüntülenemez; ziyaretçi önce bir görüntüleme isteği gönderip belge sahibinin
    onayını beklemek zorundadır."""
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('accounts:profile')

    profile, _ = Profile.objects.get_or_create(user=target_user)

    my_requests = {
        r.document_id: r
        for r in DocumentAccessRequest.objects.filter(requester=request.user, document__user=target_user)
    }
    doc_rows = [
        {'document': doc, 'access_request': my_requests.get(doc.id)}
        for doc in target_user.documents.all()
    ]

    context = {
        'target_user': target_user,
        'profile': profile,
        'doc_rows': doc_rows,
        'machines': profile.machines.all(),
    }
    return render(request, 'accounts/public_profile.html', context)


@login_required
def request_document_access_view(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if document.user == request.user:
        messages.info(request, 'Bu zaten sizin belgeniz.')
        return redirect('accounts:profile')

    access_request, created = DocumentAccessRequest.objects.get_or_create(
        document=document,
        requester=request.user,
        defaults={'status': DocumentAccessRequest.Status.PENDING},
    )

    if created:
        messages.success(request, 'Görüntüleme isteğiniz gönderildi, onay bekleniyor.')
    elif access_request.status == DocumentAccessRequest.Status.DENIED:
        access_request.status = DocumentAccessRequest.Status.PENDING
        access_request.responded_at = None
        access_request.save(update_fields=['status', 'responded_at'])
        messages.success(request, 'Görüntüleme isteğiniz tekrar gönderildi.')
    else:
        messages.info(request, 'Bu belge için zaten bir isteğiniz var.')

    return redirect('accounts:public_profile', username=document.user.username)


@login_required
def respond_document_access_view(request, pk, action):
    """action: 'approve' ya da 'deny'. Sadece belge sahibi yanıt verebilir."""
    access_request = get_object_or_404(DocumentAccessRequest, pk=pk, document__user=request.user)

    if action == 'approve':
        access_request.status = DocumentAccessRequest.Status.APPROVED
        messages.success(request, f'{access_request.requester} kullanıcısına görüntüleme izni verildi.')
    else:
        access_request.status = DocumentAccessRequest.Status.DENIED
        messages.info(request, f'{access_request.requester} kullanıcısının isteği reddedildi.')

    access_request.responded_at = timezone.now()
    access_request.save(update_fields=['status', 'responded_at'])
    return redirect('accounts:profile')


@login_required
def document_upload_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Belgeniz yüklendi.')
        else:
            messages.error(request, 'Belge yüklenirken bir hata oluştu, lütfen tekrar deneyin.')
    return redirect('accounts:profile')


@login_required
def document_delete_view(request, pk):
    document = get_object_or_404(Document, pk=pk, user=request.user)
    document.delete()
    messages.info(request, 'Belge silindi.')
    return redirect('accounts:profile')


@login_required
def machine_add_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            machine = form.save(commit=False)
            machine.profile = profile
            machine.save()
            messages.success(request, 'Makine parkurunuza eklendi.')
        else:
            messages.error(request, 'Makine eklenirken bir hata oluştu.')
    return redirect('accounts:profile')


@login_required
def machine_delete_view(request, pk):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    machine = get_object_or_404(Machine, pk=pk, profile=profile)
    machine.delete()
    messages.info(request, 'Makine kaydı silindi.')
    return redirect('accounts:profile')
