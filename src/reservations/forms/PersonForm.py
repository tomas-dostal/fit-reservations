import django.forms as forms
from django.core.validators import EmailValidator
from django.forms import ModelForm, DateTimeInput
from reservations.models import *
from reservations.services import *
from reservations.models import Person


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["name"].initial = instance.name
            self.fields["surname"].initial = instance.surname
            self.fields["is_admin"].initial = instance.is_admin
            self.fields["email"].initial = instance.email
            self.fields["password"].required = False

    name = forms.CharField(label="Jméno")
    surname = forms.CharField(label="Příjmení")
    email = forms.CharField(validators=[EmailValidator])
    is_admin = forms.BooleanField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), label="Heslo")

    class Meta:
        model = Person
        fields = ("name", "surname", "phone_number", "is_admin", "occupy")
        labels = {
            "name": "Jméno",
            "surname": "Příjmení",
            "is_admin": "Správce",
            "occupy": "Je uživatelem místností",
            "phone_number": "Telefonni cislo",
        }

    def update(self):
        model_instance = super(PersonForm, self).save(commit=False)
        result = super(PersonForm, self).save(commit=True)

        model_instance.name = self.cleaned_data["name"]
        model_instance.surname = self.cleaned_data["surname"]
        model_instance.is_admin = self.cleaned_data["is_admin"]
        model_instance.save()
        return result
