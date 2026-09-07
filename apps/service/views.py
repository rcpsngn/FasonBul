from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory


def service_list(request):
    categories = ServiceCategory.objects.all()
    services = Service.objects.filter(is_active=True)

    category_slug = request.GET.get('category')
    if category_slug:
        services = services.filter(category__slug=category_slug)

    context = {
        'categories': categories,
        'services': services,
    }
    return render(request, 'service/list.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(id=service.id)[:4]

    context = {
        'service': service,
        'other_services': other_services,
    }
    return render(request, 'service/detail.html', context)