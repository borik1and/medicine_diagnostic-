# Generated by Django 5.0.3 on 2024-03-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_service', models.CharField(max_length=200)),
                ('description_service', models.CharField(max_length=200)),
            ],
        ),
    ]