from django import forms
from .models import Order
from django.shortcuts import render

# Ваши доступные временные интервалы

TIME_CHOICES = [
    ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'),
    ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'),
    ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'),
    ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'),
    ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'),
    ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
]


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'version_flag':
                field.widget.attrs['class'] = 'form-control'


class OrderForm(StyleFormMixin, forms.ModelForm):
    order_time = forms.ChoiceField(choices=TIME_CHOICES)

    class Meta:
        model = Order
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'service', 'order_date', 'order_time')
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        time_choices = kwargs.pop('time_choices', None)
        super().__init__(*args, **kwargs)
        if time_choices:
            self.fields['order_time'].choices = time_choices


def order_form_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Обработка валидной формы
            form.save()
    else:
        form = OrderForm()

    return render(request, 'order_form.html', {'form': form})
