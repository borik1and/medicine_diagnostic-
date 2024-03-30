from django.db import models


class Main(models.Model):
    title_service = models.CharField(max_length=200, name='title_service')
    description_service = models.CharField(max_length=200, name='description_service')

    def __str__(self):
        return f'Имя: {self.title_service} email: {self.description_service}'
