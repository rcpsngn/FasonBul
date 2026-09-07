from django.urls import path
from . import views

app_name = 'fason_advert'

urlpatterns = [
    path('', views.advert_list, name='list'),
    path('yeni/', views.advert_create, name='create'),
    path('<slug:slug>/', views.advert_detail, name='detail'),
]