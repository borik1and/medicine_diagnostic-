# Generated by Django 5.0.3 on 2024-04-05 13:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_address_remove_order_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='datetime',
        ),
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]
