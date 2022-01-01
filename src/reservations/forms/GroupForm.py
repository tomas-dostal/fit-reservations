import django.forms as forms
from django.forms import ModelForm
from reservations.models import *
from reservations.services import *


class GroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance", None)
        if instance:
            self.fields["rooms"].initial = RoomService.find_rooms_for_group(instance)

    rooms = forms.ModelMultipleChoiceField(Room.objects.all(), label="Místnosti", required=False)

    class Meta:
        model = Group
        labels = {"name": "Název", "parent": "Nadřazená skupina", "member": "Členové", "manager": "Správce"}
        fields = "__all__"
