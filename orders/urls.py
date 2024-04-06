from django.urls import path

from orders.views import OrdercreateView, OrderSuccessView, OrderListView, OrderDetailView, OrderUpdateView, \
    OrderDeleteView, get_available_times

app_name = 'orders'

urlpatterns = [
    path('', OrdercreateView.as_view(), name='order-create'),
    path('order-success', OrderSuccessView.as_view(), name='order-success'),
    path('list', OrderListView.as_view(), name='list'),
    path('view/<int:pk>/', OrderDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', OrderUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete'),
    path('get-available-times/<str:date>/', get_available_times, name='get-available-times'),

]

