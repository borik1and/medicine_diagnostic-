from django.urls import path

from orders.views import OrdercreateView, OrderSuccessView

app_name = 'orders'

urlpatterns = [
    path('', OrdercreateView.as_view(), name='order-create'),
    path('order-success', OrderSuccessView.as_view(), name='order-success'),

]
