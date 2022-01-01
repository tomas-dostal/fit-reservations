import django.forms as forms
from django.forms import ModelForm, DateTimeInput
from pytz import timezone

from reservations.services import *


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
        if dt_from < datetime.now(timezone("Europe/Berlin")):
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

        if dt_from < datetime.now(timezone("Europe/Berlin")):
            raise forms.ValidationError("Start date should be greater than current date")
