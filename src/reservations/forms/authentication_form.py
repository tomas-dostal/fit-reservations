import django.forms as forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label="Username", widget=forms.TextInput(attrs={"autofocus": True}))

    password = forms.CharField(widget=forms.PasswordInput(), label="Heslo")
