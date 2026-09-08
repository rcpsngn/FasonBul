import math
from urllib.parse import quote

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Workshop
from .forms import WorkshopForm


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def workshop_search_view(request):
    workshops = Workshop.objects.all()

    search_query = request.GET.get('q', '')
    selected_city = request.GET.get('city', '')
    selected_category = request.GET.get('category', '')
    selected_distance = request.GET.get('distance', '')
    user_lat = request.GET.get('user_lat')
    user_lng = request.GET.get('user_lng')

    if search_query:
        workshops = workshops.filter(title__icontains=search_query)
    if selected_city:
        workshops = workshops.filter(city__icontains=selected_city)
    if selected_category:
        workshops = workshops.filter(category=selected_category)

    workshops = list(workshops)

    if selected_distance and user_lat and user_lng:
        try:
            user_lat = float(user_lat)
            user_lng = float(user_lng)
            max_distance = float(selected_distance)
            filtered = []
            for ws in workshops:
                if ws.latitude is not None and ws.longitude is not None:
                    dist = haversine_km(user_lat, user_lng, ws.latitude, ws.longitude)
                    if dist <= max_distance:
                        ws.calculated_distance = round(dist, 1)
                        filtered.append(ws)
            workshops = sorted(filtered, key=lambda w: w.calculated_distance)
        except (ValueError, TypeError):
            pass

    google_maps_search_url = None
    if not workshops:
        query = f"{selected_city or 'Türkiye'} fason atölyesi"
        google_maps_search_url = f"https://www.google.com/maps/search/?api=1&query={quote(query)}"

    context = {
        'workshops': workshops,
        'search_query': search_query,
        'selected_city': selected_city,
        'selected_category': selected_category,
        'selected_distance': selected_distance,
        'category_choices': Workshop.CATEGORY_CHOICES,
        'google_maps_search_url': google_maps_search_url,
        'external_workshops': None,
    }
    return render(request, 'workshop/list.html', context)


@login_required
def workshop_create_view(request):
    if request.method == 'POST':
        form = WorkshopForm(request.POST, request.FILES)
        if form.is_valid():
            workshop = form.save(commit=False)
            workshop.owner = request.user
            workshop.save()
            return redirect('workshop:detail', pk=workshop.pk)
    else:
        form = WorkshopForm()

    context = {
        'form': form,
    }
    return render(request, 'workshop/form.html', context)


def workshop_detail_view(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    profile = getattr(workshop.owner, 'profile', None)
    machines = profile.machines.all() if profile is not None else []

    context = {
        'workshop': workshop,
        'machines': machines,
    }
    return render(request, 'workshop/detail.html', context)


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


