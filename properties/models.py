from django.db import models
from django.conf import settings


class Property(models.Model):
    LISTING_TYPE = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    )

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        limit_choices_to={'role': 'agent'},
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE, default='sale')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.city})"
