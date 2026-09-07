from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Advert, AdvertCategory
from .forms import AdvertForm


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

    context = {
        'advert': advert,
        'related_adverts': related_adverts,
    }
    return render(request, 'fason_advert/detail.html', context)


@login_required
def advert_create(request):
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