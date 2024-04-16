from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView
from django.urls import path

from django.views.generic import TemplateView

from users.views import ProfileView, EmailConfirmationSentView, \
    UserConfirmEmailView, EmailConfirmedView, EmailConfirmationFailedView, CustomPasswordResetView

app_name = 'users'

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'),
         name='invalid_verify'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
]
