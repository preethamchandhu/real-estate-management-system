from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.property_list, name='list'),
    path('mine/', views.agent_property_list, name='agent_list'),
    path('add/', views.property_create, name='create'),
    path('<int:pk>/', views.property_detail, name='detail'),
    path('<int:pk>/edit/', views.property_update, name='update'),
    path('<int:pk>/delete/', views.property_delete, name='delete'),
    path('<int:pk>/documents/add/', views.property_add_document, name='add_document'),
]
