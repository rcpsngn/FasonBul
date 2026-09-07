from django.shortcuts import render
from .models import Banner, Statistic
from apps.fason_advert.models import Advert
from apps.service.models import Service
from apps.blog.models import Post


def index_view(request):
    banners = Banner.objects.filter(is_active=True)
    statistics = Statistic.objects.filter(is_active=True)

    # Diğer uygulamalardan öne çıkan / son eklenen içerikleri çekiyoruz
    latest_adverts = Advert.objects.filter(is_active=True)[:6]
    services = Service.objects.filter(is_active=True)[:4] if hasattr(Service, 'is_active') else Service.objects.all()[
                                                                                                :4]
    latest_posts = Post.objects.filter(is_published=True)[:3] if hasattr(Post, 'is_published') else Post.objects.all()[
                                                                                                    :3]

    context = {
        'banners': banners,
        'statistics': statistics,
        'latest_adverts': latest_adverts,
        'services': services,
        'latest_posts': latest_posts,
    }
    return render(request, 'mainpage/index.html', context)