from django.shortcuts import render, redirect
from .models import Workshop
from .forms import WorkshopForm


def workshop_search_view(request):
    latest_adverts = Workshop.objects.all().order_by('-created_at')[:6]
    context = {
        'latest_adverts': latest_adverts,
    }
    return render(request, 'mainpage/index.html', context)


def workshop_create_view(request):
    if request.method == 'POST':
        form = WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('workshop:list')
    else:
        form = WorkshopForm()

    context = {
        'form': form,
    }
    # Dosya adınız 'form.html' olduğu için burayı güncelliyoruz:
    return render(request, 'workshop/form.html', context)


def google_maps_search_view(request):
    city = request.GET.get('city', 'İstanbul')
    category = request.GET.get('category', 'Tekstil Fason')
    search_query = f"{city} {category} fason atolyesi"

    context = {
        'search_query': search_query,
        'city': city,
        'category': category,
    }
    return render(request, 'workshop/map_search.html', context)