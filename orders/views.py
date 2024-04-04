from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.forms import OrderForm
from orders.models import Order


class OrdercreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('main:main_list')
