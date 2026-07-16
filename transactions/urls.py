from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('request/<int:property_id>/', views.request_transaction, name='request'),
    path('mine/', views.my_transactions, name='my_transactions'),
    path('agent/', views.agent_transactions, name='agent_transactions'),
    path('agent/<int:pk>/<str:new_status>/', views.update_transaction_status, name='update_status'),
]
