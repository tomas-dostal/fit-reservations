from django.contrib.auth.models import User
from rest_framework import serializers

from reservations.models import Person, Building, Group, Room, Reservation, ReservationStatus


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ("password", "last_name", "first_name", "is_superuser", "email", "username")
        extra_kwargs = {
            'username': {'validators': []},
        }

    def create(self, validated_data):
        if 'password' not in validated_data:
            validated_data['password'] = "samplepassword"
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
        user.save()
        return user


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)

    class Meta:
        model = Person
        fields = ("occupy", "user", "phone_number")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        original_user_data = self.initial_data.get('user')
        user_serializer = UserSerializer(data=original_user_data)
        user_serializer.is_valid(raise_exception=True)
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        validated_data['user'] = user
        return super(PersonSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_data = validated_data.pop('user')
            original_user_data = self.initial_data.get('user')
            user_serializer = UserSerializer(data=original_user_data)
            user_serializer.is_valid(raise_exception=True)
            user = UserSerializer.update(UserSerializer(), instance=instance.user, validated_data=user_data)
            validated_data['user'] = user
        return super(PersonSerializer, self).update(instance, validated_data)


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ("name", )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", "parent", "manager", "member")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("name", "building", "group", "manager", "locked")


class ReservationStatusSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReservationStatus
        fields = ("status", "note", "author", "dt_modified")

    def create(self, validated_data):
        reservation_status = ReservationStatus.objects.create(
            author=Person.objects.get(user=self.context['request'].user),
            **validated_data
        )
        return reservation_status


class ReservationSerializer(serializers.ModelSerializer):
    note = serializers.CharField(read_only=True, required=False)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ("room", "attendees", "author", "owner", "reservation_status", "dt_from", "dt_to", "dt_created", "note")

    def create(self, validated_data):
        attendees = validated_data.pop("attendees")
        reservation = Reservation.objects.create(
            author=Person.objects.get(user=self.context['request'].user),
            **validated_data
        )
        reservation.attendees.set(attendees)
        return reservation

    def update(self, instance, validated_data):
        attendees = validated_data.pop("attendees")
        Reservation.objects.filter(pk=instance.id).update(
            author=Person.objects.get(user=self.context['request'].user),
            **validated_data
        )
        reservation = Reservation.objects.get(pk=instance.id)
        reservation.attendees.set(attendees)
        return reservation
