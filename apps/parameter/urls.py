from django.urls import path
from . import views

app_name = 'parameter'

urlpatterns = [
    path('get-districts/<int:city_id>/', views.get_districts, name='get_districts'),
]