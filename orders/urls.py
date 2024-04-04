from django.urls import path

from orders.views import OrdercreateView

app_name = 'orders'

urlpatterns = [
    path('', OrdercreateView.as_view(), name='order-create'),

]
