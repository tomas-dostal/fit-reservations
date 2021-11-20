import django.forms as forms
from django.forms import ModelForm
from reservations.models import *

from reservations.services import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = "__all__"
