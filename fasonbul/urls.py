from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Proje Uygulama Rotaları
    path('', include('apps.mainpage.urls', namespace='mainpage')),
    path('hesap/', include('apps.accounts.urls', namespace='accounts')),
    path('atolye/', include('apps.workshop.urls', namespace='workshop')),
    path('ilanlar/', include('apps.fason_advert.urls', namespace='fason_advert')),
    path('hakkimizda/', include('apps.about.urls', namespace='about')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('iletisim/', include('apps.contracts.urls', namespace='contracts')),
    path('hizmetler/', include('apps.service.urls', namespace='service')),
    path('mesajlar/', include('apps.chat.urls', namespace='chat')),
]

# Geliştirme (DEBUG) ortamında yüklenen resim/medya dosyalarının görüntülenebilmesi için:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)