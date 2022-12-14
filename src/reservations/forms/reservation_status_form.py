from django.forms import ModelForm

from reservations.services import *


class ReservationStatusForm(ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ["status", "note"]
