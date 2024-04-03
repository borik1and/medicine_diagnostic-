from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from users.forms import UserRegisterForm, UserProfileForm, AuthenticationForm
from users.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from config import settings
from django.contrib.auth.forms import PasswordResetForm
from django.views.generic.edit import FormView


MyUser = get_user_model()
UserModel = get_user_model()


class MyLoginView(LoginView):
    form_class = AuthenticationForm


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        current_site = get_current_site(self.request)

        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site.domain}{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = MyUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class CustomPasswordResetView(FormView):
    template_name = 'users/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = '/users/'

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            user = UserModel.objects.get(email__iexact=email, is_active=True)
        except UserModel.DoesNotExist:
            # Обработка случая, когда пользователь не найден
            return self.form_invalid(form)

        # Генерация нового пароля
        new_password = UserModel.objects.make_random_password()
        user.set_password(new_password)
        user.save()

        # Отправка нового пароля на почту
        subject = 'Ваш новый пароль'
        message = f'Ваш новый пароль: {new_password}'
        send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[user.email])

        return super().form_valid(form)

