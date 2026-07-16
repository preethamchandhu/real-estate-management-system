from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=15, blank=True)

    def is_admin_role(self):
        return self.role == 'admin' or self.is_superuser

    def is_agent(self):
        return self.role == 'agent'

    def is_client(self):
        return self.role == 'client'

    def __str__(self):
        return f"{self.username} ({self.role})"
