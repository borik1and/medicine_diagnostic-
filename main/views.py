from django.views.generic import ListView

from main.models import Main


class MainView(ListView):
    model = Main


class AboutView(ListView):
    model = Main
    template_name = 'main/about.html'


class ServicesView(ListView):
    model = Main
    template_name = 'main/services.html'
