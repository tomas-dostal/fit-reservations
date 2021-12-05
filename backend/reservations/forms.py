import django.forms as forms
from django.forms import ModelForm, DateTimeInput
from reservations.models import *
from reservations.services import *


class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            self.name = instance.name
            self.surname = instance.surname
            self.is_admin = instance.surname
        super().__init__(*args, **kwargs)

    name = forms.CharField()
    surname = forms.CharField()
    is_admin = forms.BooleanField()

    class Meta:
        model = Person
        fields = ("name", "surname", "is_admin", "occupy")
        labels = {"name": "Jméno", "surname": "Příjmení", "is_admin": "Správce", "occupy": "Je uživatelem místností"}

    def update(self):
        model_instance = super(PersonForm, self).save(commit=False)
        result = super(PersonForm, self).save(commit=True)

        model_instance.name = self.cleaned_data['name']
        model_instance.surname = self.cleaned_data['surname']
        model_instance.is_admin = self.cleaned_data['is_admin']
        model_instance.save()
        return result


class BuildingForm(ModelForm):
    class Meta:
        model = Building
        labels = {"name": "Název budovy"}
        fields = "__all__"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"


class RoomForm(ModelForm):
    class Meta:
        model = Room
        labels = {"name": "Název místnosti", "building": "Budova", "group": "Skupina", "manager": "Správce"}
        fields = "__all__"


class ReservationStatusForm(ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ["status", "note"]


class AdminReservationForm(ModelForm):
    note = forms.CharField(widget=forms.Textarea(), label="Poznámka")

    class Meta:
        model = Reservation
        # TODO: Add owner field, author=currentUser
        fields = ["author", "attendees", "room", "dt_from", "dt_to"]
        labels = {
            "author": "Autor",
            "attendees": "Uživatelé",
            "room": "Místnost",
            "fd_from": "Platnost od",
            "fd_to": "Platnost do",
        }
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


class ReservationForm(ModelForm):
    note = forms.CharField(widget=forms.Textarea(), label="Poznámka")

    class Meta:
        model = Reservation
        # TODO: author=currentUser, owner = currectUser, room - display only rooms available for currentUser
        fields = ["author", "attendees", "room", "dt_from", "dt_to"]
        labels = {
            "author": "Autor",
            "attendees": "Uživatelé",
            "room": "Místnost",
            "fd_from": "Platnost od",
            "fd_to": "Platnost do",
        }
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
