from django.urls import path

from main.views import MainView, AboutView, ServicesView

app_name = 'main'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('about/', AboutView.as_view(), name='about'),
    path('services/', ServicesView.as_view(), name='services'),
]
