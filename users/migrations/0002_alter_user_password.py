# Generated by Django 5.0.3 on 2024-04-03 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default=' ', max_length=50, verbose_name='password'),
        ),
    ]
