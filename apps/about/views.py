from django.shortcuts import render
from .models import AboutPage, Statistic


def about_view(request):
    about_data = AboutPage.objects.first()
    statistics = Statistic.objects.all()

    context = {
        'about': about_data,
        'statistics': statistics,
    }
    return render(request, 'about/login.html', context)