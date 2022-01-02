from django.contrib.auth.views import LoginView

from reservations.forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
