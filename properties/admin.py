from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'agent', 'city', 'listing_type', 'price', 'status', 'created_at')
    list_filter = ('listing_type', 'status', 'city')
    search_fields = ('title', 'city', 'address')
