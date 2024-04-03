from django import forms

from orders.models import Order


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'version_flag':
                field.widget.attrs['class'] = 'form-control'


class OrderForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
