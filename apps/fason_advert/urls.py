from django.urls import path
from . import views

app_name = 'fason_advert'

urlpatterns = [
    path('', views.advert_list, name='list'),
    path('yeni/', views.advert_create, name='create'),
    path('tekliflerim/', views.my_proposals_view, name='my_proposals'),
    path('teklif/<int:pk>/kabul-et/', views.proposal_respond_view, {'action': 'accept'}, name='proposal_accept'),
    path('teklif/<int:pk>/reddet/', views.proposal_respond_view, {'action': 'reject'}, name='proposal_reject'),
    path('teklif/<int:pk>/geri-cek/', views.proposal_withdraw_view, name='proposal_withdraw'),

    # Bunlar '<slug:slug>/' genel yakalayıcısından ÖNCE tanımlanmalı
    path('<slug:slug>/teklif-ver/', views.proposal_create_view, name='proposal_create'),
    path('<slug:slug>/teklifler/', views.advert_proposals_view, name='advert_proposals'),
    path('<slug:slug>/', views.advert_detail, name='detail'),
]
