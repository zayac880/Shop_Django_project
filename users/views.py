import random

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


from users.forms import UserRegisterForm, UserRedactForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()


        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        current_site = get_current_site(self.request)
        activation_link = f"http://{current_site.domain}/users/activate/{uid}/{token}/"


        send_mail(
            subject='Подтверждение регистрации',
            message=f'Следуйте по ссылке для подтверждения регистрации: {activation_link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class RedactView(UpdateView):
    model = User
    form_class = UserRedactForm
    success_url = reverse_lazy('users:redact')

    def get_object(self, queryset=None):
        return self.request.user


def generate_password(request):
    new_password = ''.join([str(random.randint(0,9)) for _ in range(12)])
    send_mail(
        subject='Пароль изменен!',
        message=f'Новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]

    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if not User.objects.filter(email=user.email, is_active=True).exists():
            user.is_active = True
            user.save()
            return redirect(reverse('users:login'))
        else:
            messages.error(request, 'Аккаунт с этим email уже активирован.')
            return redirect(reverse('users:account_activation_failed'))
    else:
        return redirect(reverse('users:account_activation_failed'))

