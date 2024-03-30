from django.views.generic import ListView

from main.models import Main


class MainView(ListView):
    model = Main
