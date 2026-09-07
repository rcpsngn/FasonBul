from django.urls import path
from . import views

app_name = 'workshop'

urlpatterns = [
    path('', views.workshop_search_view, name='list'),
    path('ekle/', views.workshop_create_view, name='create'),
    path('harita/', views.google_maps_search_view, name='map_search'),
]
