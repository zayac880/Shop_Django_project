import random

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail
from django.conf import settings


from users.forms import UserRegisterForm, UserRedactForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()

        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Вы зарегистрировались и бла бла бла:)',
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
