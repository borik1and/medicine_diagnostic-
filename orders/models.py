from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

SERVICE_CHOICES = (
    ('X-Ray Services', 'X-Ray Services'),
    ('MRI Services', 'MRI Services'),
    ('Scan Services', 'Scan Services')
)


class Order(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, **NULLABLE)
    last_name = models.CharField(max_length=100, **NULLABLE)
    phone_number = models.CharField(max_length=20, **NULLABLE)
    address = models.CharField(max_length=250, **NULLABLE)
    city = models.CharField(max_length=50, **NULLABLE)
    state = models.CharField(max_length=50, **NULLABLE)
    country = models.CharField(max_length=50, **NULLABLE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
