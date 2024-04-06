from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import User

NULLABLE = {'blank': True, 'null': True}

SERVICE_CHOICES = (
    ('X-Ray', 'X-Ray'),
    ('MRI', 'MRI'),
    ('CT', 'CT')
)

TIME_CHOICES = [
    ('09:00:00', '09:30:00'),
    ('09:31:00', '10:00:00'),
    ('10:01:00', '10:30:00'),
    ('10:31:00', '11:00:00'),
    ('11:01:00', '11:30:00'),
    ('11:31:00', '12:00:00'),
    ('12:01:00', '12:30:00'),
    ('12:31:00', '13:00:00'),
    ('13:01:00', '13:30:00'),
    ('13:31:00', '14:00:00'),
    ('14:01:00', '14:30:00'),
    ('14:31:00', '15:00:00'),
    ('15:01:00', '15:30:00'),
    ('15:31:00', '16:00:00'),
    ('16:01:00', '16:30:00'),
    ('16:31:00', '17:00:00'),
    ('17:01:00', '17:30:00'),
    ('17:31:00', '18:00:00'),
    ('18:01:00', '18:30:00'),
    ('18:31:00', '19:00:00'),
    ('19:01:00', '19:30:00'),
    ('19:31:00', '20:00:00'),
    ('20:01:00', '20:30:00'),
    ('20:31:00', '21:00:00'),
]


class Order(models.Model):
    email = models.EmailField(max_length=250)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=100, **NULLABLE)
    phone_number = models.CharField(max_length=20, **NULLABLE)
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    order_date = models.DateField(default=timezone.now)
    order_time = models.TimeField(choices=TIME_CHOICES)
