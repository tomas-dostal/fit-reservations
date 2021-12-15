import django.forms as forms
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
    email = forms.CharField()
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
    # TODO This needs to be the logged in user later when logging in works.
    author = forms.ModelChoiceField(queryset=Person.objects.all())

    class Meta:
        model = ReservationStatus
        fields = ["status", "note"]


class AdminReservationForm(ModelForm):
    note = forms.CharField(widget=forms.Textarea(), label="Poznámka")

    class Meta:
        model = Reservation
        # TODO: Add owner field, author=currentUser
        fields = ["owner", "attendees", "room", "dt_from", "dt_to"]
        labels = {
            "owner": "Vlastník",
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
        fields = ["attendees", "room", "dt_from", "dt_to"]
        labels = {
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
