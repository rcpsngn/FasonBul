from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('<int:conversation_pk>/duzenle/', views.contract_edit_view, name='contract_edit'),
    path('<int:conversation_pk>/onayla/', views.contract_approve_view, name='contract_approve'),
    path('<int:conversation_pk>/tamamlandi/', views.contract_complete_view, name='contract_complete'),
    path('<int:conversation_pk>/', views.contract_detail_view, name='contract_detail'),
]
