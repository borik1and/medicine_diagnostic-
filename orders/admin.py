from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'order_date', 'order_time', 'service')
    list_filter = ('email', 'first_name', 'last_name', 'order_date', 'order_time', 'phone_number', 'service')
