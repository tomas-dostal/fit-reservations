import django.forms as forms
from django.forms import ModelForm, SelectDateWidget, DateInput, DateTimeInput
from reservations.models import *
from reservations.services import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ("name", "surname", "is_admin", "occupy")
        labels = {"name": "Jméno", "surname": "Příjmení", "is_admin": "Správce", "occupy": "Je uživatelem místností"}


class BuildingForm(ModelForm):
    class Meta:
        model = Building
        labels = {"name": "Název budovy"}
        fields = "__all__"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(GroupForm, self).__init__(*args, **kwargs)
        # Parent is not required.
        self.fields['parent'].required = False


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"


class ReservationStatusForm(ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ["status", "note"]


class ReservationForm(ModelForm):
    note = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Reservation
        fields = ["author", "attendees", "room", "dt_from", "dt_to"]
        widgets = {
            "dt_from": DateTimeInput(attrs={"type": "datetime-local"}),
            "dt_to": DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        dt_from = cleaned_data.get("dt_from")
        dt_to = cleaned_data.get("dt_to")
        if dt_to < dt_from:
            raise forms.ValidationError("End date should be greater than start date.")
