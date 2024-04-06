from django import forms
import datetime

from orders.models import Order

TIME_CHOICES = [
    '09:00',
    '09:30',
    '10:00',
    '10:30',
    '11:00',
    '11:30',
    '12:00',
    '12:30',
    '13:00',
    '13:30',
    '14:00',
    '14:30',
    '15:00',
    '15:30',
    '16:00',
    '16:30',
    '17:00',
    '17:30',
    '18:00',
    '18:30',
    '19:00',
    '19:30',
    '20:00',
    '20:30',
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'version_flag':
                field.widget.attrs['class'] = 'form-control'


class OrderForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'service', 'order_date', 'order_time')
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        selected_date = cleaned_data.get('order_date')
        print(selected_date)
        if selected_date:
            # Получаем все заказы на выбранную дату
            orders_on_date = Order.objects.filter(order_date=selected_date)
            booked_starts = [order.order_time for order in orders_on_date]
            print('orders_on_date:', orders_on_date)
            print('booked_starts', booked_starts)

            # Если на выбранную дату нет заказов, используем все доступные временные интервалы из TIME_CHOICES
            if not orders_on_date:
                available_times = [(time, time) for time in TIME_CHOICES]
            else:
                # Формируем доступные временные интервалы на основе TIME_CHOICES и уже забронированных времен
                available_times = [(time, time) for time in TIME_CHOICES if time not in booked_starts]
            print('available_times:', available_times)
            self.fields['order_time'].choices = available_times
        return cleaned_data
