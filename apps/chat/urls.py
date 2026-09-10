from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox_view, name='inbox'),
    path('<int:pk>/', views.conversation_detail_view, name='conversation_detail'),
    path('<int:pk>/gorusme-onayla/', views.confirm_meeting_view, name='confirm_meeting'),
]
