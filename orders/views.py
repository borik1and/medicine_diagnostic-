from django.contrib.auth.forms import UserModel
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from config import settings
from orders.models import Order
from users.models import User
from orders.forms import OrderForm
from django.http import JsonResponse

# Ваши доступные временные интервалы

TIME_CHOICES = [
    ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'),
    ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'),
    ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'),
    ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'),
    ('17:00', '17:00'), ('17:30', '17:30'), ('18:00', '18:00'), ('18:30', '18:30'),
    ('19:00', '19:00'), ('19:30', '19:30'), ('20:00', '20:00'), ('20:30', '20:30'),
]


class OrdercreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:order-success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['time_choices'] = TIME_CHOICES
        return kwargs

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


class OrderListView(ListView):
    model = Order


class OrderDetailView(DetailView):
    model = Order


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create.html'
    success_url = reverse_lazy('orders:list')
    queryset = Order.objects.all()

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('orders:view', args=[self.kwargs.get('pk')])


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


def get_available_times(request):
    selected_date = request.GET.get('selected_date')

    if not selected_date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    orders_on_date = Order.objects.filter(order_date=selected_date)
    booked_starts = [order.order_time.strftime('%H:%M') for order in orders_on_date]
    time_choices_strings = [time for time, _ in TIME_CHOICES]
    available_times = [(time, time) for time in time_choices_strings if time not in booked_starts]

    return JsonResponse({'available_times': available_times})
