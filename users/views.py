from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserRedactForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class RedactView(UpdateView):
    model = User
    form_class = UserRedactForm
    success_url = reverse_lazy('users:redact')

    def get_object(self, queryset=None):
        return self.request.user
