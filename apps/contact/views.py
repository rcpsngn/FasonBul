from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm
from .models import ContactInfo


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajınız başarıyla iletildi. En kısa sürede dönüş yapacağız.')
            return redirect('contact:index')
    else:
        form = ContactForm()

    info = ContactInfo.objects.first()

    context = {
        'form': form,
        'info': info,
    }
    return render(request, 'contact/contact.html', context)