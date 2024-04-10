from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}

SERVICE_CHOICES = (
    ('X-Ray', 'X-Ray'),
    ('MRI', 'MRI'),
    ('CT', 'CT')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=100, **NULLABLE)
    phone_number = models.CharField(max_length=20, **NULLABLE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    order_date = models.DateField(default=timezone.now)
    order_time = models.TimeField(default=None, **NULLABLE)
