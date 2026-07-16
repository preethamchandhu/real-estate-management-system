from django.db import models
from django.conf import settings
from properties.models import Property


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('buy', 'Buy'),
        ('rent', 'Rent'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        limit_choices_to={'role': 'client'},
    )
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client} - {self.property} ({self.status})"
