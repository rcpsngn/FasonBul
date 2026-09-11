from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('sozlesme/<int:contract_pk>/degerlendir/', views.review_create_view, name='review_create'),
]
