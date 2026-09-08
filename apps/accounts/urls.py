from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('kayit/', views.register_view, name='register'),
    path('giris/', views.login_view, name='login'),
    path('cikis/', views.logout_view, name='logout'),
    path('profil/', views.profile_view, name='profile'),
    path('belge/yukle/', views.document_upload_view, name='document_upload'),
    path('belge/<int:pk>/sil/', views.document_delete_view, name='document_delete'),
    path('makine/ekle/', views.machine_add_view, name='machine_add'),
    path('makine/<int:pk>/sil/', views.machine_delete_view, name='machine_delete'),
    path('ara/', views.user_search_view, name='user_search'),

    # Belge görüntüleme izin akışı
    path('profil/<str:username>/', views.public_profile_view, name='public_profile'),
    path('belge/<int:pk>/istek-gonder/', views.request_document_access_view, name='document_request_access'),
    path('istek/<int:pk>/onayla/', views.respond_document_access_view, {'action': 'approve'}, name='document_request_approve'),
    path('istek/<int:pk>/reddet/', views.respond_document_access_view, {'action': 'deny'}, name='document_request_deny'),
]
