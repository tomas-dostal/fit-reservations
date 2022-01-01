from django.forms import ModelForm
from reservations.models import *
from reservations.services import *


class RoomForm(ModelForm):
    class Meta:
        model = Room
        labels = {"name": "Název místnosti", "building": "Budova", "group": "Skupina", "manager": "Správce"}
        fields = ["name", "building", "group", "manager"]


class RoomGroupManagerForm(ModelForm):
    class Meta:
        model = Room
        fields = ["manager"]
        labels = {
            "manager": "Správce",
        }
