from django.contrib.auth.forms import UserModel
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from config import settings
from orders.models import Order
from users.models import User
from orders.forms import OrderForm


class OrdercreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:order-success')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        service = form.cleaned_data['service']
        first_name = form.cleaned_data['first_name']

        # Проверяем, существует ли пользователь с таким email
        try:
            user = User.objects.get(email=email)
            order = Order.objects.create(email=email, service=service, first_name=first_name)
            subject = 'New order has been created | Medical Diagnostic Services'
            message = (f'Dear {order.first_name},\n'
                       f' Thank you for order. \n '
                       f'Your appointment details: \n'
                       f' Type of service: {order.service} \n'
                       f' Date: \n'
                       f' Time: \n'
                       f'To check your results or to cancel an appointment, please log in to our system and use your'
                       f' email address and the following password')
            send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])
        except UserModel.DoesNotExist:
            # Если пользователь не существует, создаем нового пользователя
            user = User.objects.create(email=email, is_active=True)
            order = Order.objects.create(email=email, service=service, first_name=first_name)

            # Генерируем случайный пароль
            new_password = UserModel.objects.make_random_password()
            user.set_password(new_password)
            user.save()

            # Отправляем письмо с паролем
            subject = 'New order has been created | Medical Diagnostic Services'
            message = (f'Dear {order.first_name},\n'
                       f' Thank you for order. \n '
                       f'Your appointment details: \n'
                       f' Type of service: {order.service} \n'
                       f' Date: \n'
                       f' Time: \n'
                       f'To check your results or to cancel an appointment, please log in to our system and use your'
                       f' email address and the following password: {new_password}')

            send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[email])

        # Создаем заказ
        order = form.save(commit=False)
        order.user = user
        order.save()

        return super().form_valid(form)


class OrderSuccessView(ListView):
    model = Order
    template_name = 'orders/order_success.html'
