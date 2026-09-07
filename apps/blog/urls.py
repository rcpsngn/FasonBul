from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('kategori/<slug:category_slug>/', views.post_list, name='category_list'),
    path('<slug:slug>/', views.post_detail, name='detail'),
]