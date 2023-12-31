from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, RedactView, generate_password, activate_account

app_name = UsersConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('redact/', RedactView.as_view(), name='redact'),
    path('redact/genpassword/', generate_password, name='generate_password'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
]