from django.urls import path

from main.views import MainView

app_name = 'main'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
]