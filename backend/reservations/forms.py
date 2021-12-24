from datetime import datetime
import django.forms as forms
from django.core.validators import EmailValidator
from django.forms import ModelForm, DateTimeInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from pytz import timezone
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


class BuildingForm(ModelForm):
    class Meta:
        model = Building
        labels = {"name": "Název budovy"}
        fields = "__all__"


class GroupForm(ModelForm):
    class Meta:
        model = Group
        labels = {"name": "Název", "parent": "Nadřazená skupina", "member": "Členové", "manager": "Správce"}
        fields = "__all__"


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


class ReservationStatusForm(ModelForm):
    class Meta:
        model = ReservationStatus
        fields = ["status", "note"]


class AdminReservationForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if request.user.is_superuser:
            self.fields["room"].queryset = RoomService.find_all()
        else:
            self.fields["room"].queryset = RoomService.find_managed_rooms(request.user)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["note"].initial = instance.reservation_status.last().note

    note = forms.CharField(widget=forms.Textarea(), label="Poznámka")
    room = forms.ModelChoiceField(Room.objects.none(), label="Místnost")

    class Meta:
        model = Reservation
        fields = ["owner", "room", "attendees", "dt_from", "dt_to"]
        labels = {
            "room": "Místnost",
            "owner": "Vlastník",
            "attendees": "Uživatelé",
            "dt_from": "Platnost od",
            "dt_to": "Platnost do",
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
        if dt_from < datetime.now(timezone('Europe/Berlin')):
            raise forms.ValidationError("Start date should be greater than current date")


class ReservationForm(ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["room"].queryset = RoomService.find_all_reservable_rooms(request.user)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["room"].initial = instance.room
            self.fields["note"].initial = instance.reservation_status.last().note

    note = forms.CharField(widget=forms.Textarea(), label="Poznámka")
    room = forms.ModelChoiceField(Room.objects.none(), label="Místnost")

    class Meta:
        model = Reservation
        fields = ["attendees", "dt_from", "dt_to"]
        labels = {
            "attendees": "Uživatelé",
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

        if dt_from < datetime.now(timezone('Europe/Berlin')):
            raise forms.ValidationError("Start date should be greater than current date")


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label="Username", widget=forms.TextInput(attrs={"autofocus": True}))

    password = forms.CharField(widget=forms.PasswordInput(), label="Heslo")
