from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from properties.views import property_list
from accounts.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', property_list, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('properties/', include('properties.urls')),
    path('transactions/', include('transactions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
