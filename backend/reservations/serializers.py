from rest_framework import serializers

from reservations.models import Person, Building, Group, Room, Reservation, ReservationStatus


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("name", "surname", "is_admin")


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "name"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "subgroup", "manager")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("name", "building", "group", "manager")


class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStatus
        fields = ("status", "note", "author", "dt_modified")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("room", "attendees", "author", "reservation_status", "dt_from", "dt_to", "dt_created")
