import django.forms as forms
from django.forms import ModelForm
from reservations.models import *

from reservations.services import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'surname', 'is_admin', "occupy")
        labels = {
            'name': "Jméno",
            "surname": "Příjmení",
            "is_admin": "Správce",
            "occupy": "Je uživatelem místností"
        }
