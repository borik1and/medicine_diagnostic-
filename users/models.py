from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, name='email')

    phone = models.CharField(max_length=35, name='phone', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', name='avatar', **NULLABLE)
    country = models.CharField(max_length=50, name='country', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='is_active')
    password = models.CharField(max_length=50, default=' ')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []