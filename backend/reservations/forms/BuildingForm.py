from django.forms import ModelForm
from reservations.models import *
from reservations.services import *


class BuildingForm(ModelForm):
    class Meta:
        model = Building
        labels = {"name": "Název budovy"}
        fields = "__all__"