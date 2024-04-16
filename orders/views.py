from django.contrib.auth.forms import UserModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from config import settings
from orders.models import Order
from users.models import User
from orders.forms import OrderForm, TIME_CHOICES
from django.http import JsonResponse

SUBJECT = 'Your appointment has been confirmed | Medical Diagnostic Services'


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
        order_date = form.cleaned_data['order_date']
        order_time = form.cleaned_data['order_time']

        # Проверяем, существует ли пользователь с таким email
        try:
            user = User.objects.get(email=email)
            order = Order.objects.create(email=email, service=service, first_name=first_name, order_date=order_date,
                                         order_time=order_time)
            # Генерируем случайный пароль
            new_password = UserModel.objects.make_random_password()
            user.set_password(new_password)
            user.save()

            subject = SUBJECT
            message = (f'Hey {order.first_name},\n'
                       f' Thank you for scheduling with us.\n '
                       f'Your appointment details:\n'
                       f' Type of service: {order.service}\n'
                       f' Date: {order.order_date}\n'
                       f' Time: {order.order_time}\n'
                       f'To check your results or to cancel an appointment, please log in to our system and use your'
                       f' email address and the following password: {new_password}')
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
            subject = SUBJECT
            message = (f'Hey {order.first_name},\n'
                       f' Thank you for scheduling with us.\n '
                       f'Your appointment details:\n'
                       f' Type of service: {order.service}\n'
                       f' Date: {order.order_date}\n'
                       f' Time: {order.order_time}\n'
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


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 10  # Количество заказов на одной странице

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        return self.model.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

    def get_queryset(self):
        # Возвращаем только заказы текущего пользователя
        return self.model.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Проверяем, что пользователь имеет доступ к заказу
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj


class OrderUpdateView(LoginRequiredMixin, UpdateView):
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


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


def get_available_times(request):
    selected_date = request.GET.get('selected_date')

    if not selected_date:
        return JsonResponse({'error': 'No date provided'}, status=400)

    orders_on_date = Order.objects.filter(order_date=selected_date)
    booked_starts = [order.order_time.strftime('%H:%M') for order in orders_on_date if order.order_time]
    time_choices_strings = [time for time, _ in TIME_CHOICES]
    available_times = [(time, time) for time in time_choices_strings if time not in booked_starts]

    return JsonResponse({'available_times': available_times})
