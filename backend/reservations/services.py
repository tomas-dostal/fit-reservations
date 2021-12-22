from datetime import datetime, timedelta

from .models import *
from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.utils import IntegrityError


class PersonService:
    @staticmethod
    def find_by_id(user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Person.objects.all()

    @staticmethod
    def create(data):
        try:
            user = User.objects.create(
                username=data.get("email", "test2@email.com"),
                first_name=data.get("name"),
                last_name=data.get("surname"),
                email=data.get("email", "test2@email.com"),
                is_superuser=True if data.get("is_admin") else False,
            )
            # because this is setting the RAW password, in the constructor is used hash of the password
            user.set_password(data.get("password"))
            user.save()
            person = Person.objects.create(
                user=user,
                phone_number=data.get("phone_number"),
            )
            person.occupy.set(data.get("occupy"))
            person.save()

        except IntegrityError:
            return None

        return person

    @staticmethod
    def delete(user_id):
        try:
            Person.delete(Person.objects.get(pk=user_id))
            return True
        except Person.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(person, data):
        try:
            user = person.user
            if data.get("password"):
                user.set_password(data.get("password"))
            person.user.username = data.get("email", "test2@email.com")
            person.user.first_name = data.get("name")
            person.user.last_name = data.get("surname")
            person.user.email = data.get("email", "test2@email.com")
            person.user.is_superuser = True if data.get("is_admin") else False
            person.user.save()

            person.phone_number = data.get("phone_number")
            person.occupy.set(data.get("occupy"))

            person.save()

            return True
        except Person.DoesNotExist:
            return False


class BuildingService:
    @staticmethod
    def find_by_id(building_id):
        try:
            return Building.objects.get(pk=building_id)
        except Building.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Building.objects.all()

    @staticmethod
    def save(building):
        building.save()
        return

    @staticmethod
    def delete(building_id):
        try:
            Building.delete(Building.objects.get(pk=building_id))
            return True
        except Building.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(building_id, updated_building):
        try:
            Building.objects.get(pk=building_id).update(name=updated_building.name)
            return True
        except Building.DoesNotExist:
            return False


class GroupService:
    @staticmethod
    def find_by_id(group_id):
        try:
            return Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Group.objects.all()

    @staticmethod
    def save(form):
        form.save()
        manager = form.cleaned_data.get("manager")
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename="is_group_manager"))
            manager.user.save()
        return

    @staticmethod
    def delete(group_id):
        try:
            group = Group.objects.get(pk=group_id)
            manager = group.manager
            if manager:
                managed_groups = Group.objects.filter(manager=manager)
                if len(managed_groups) < 2:
                    manager.user.user_permissions.remove(Permission.objects.get(codename="is_group_manager"))
                manager.user.save()
            Room.delete(group)
            return True
        except Group.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(form, old_group):
        try:
            old_manager = old_group.manager
            if old_manager:
                managed_groups = Group.objects.filter(manager=old_manager)
                if len(managed_groups) < 2:
                    old_manager.user.user_permissions.remove(Permission.objects.get(codename="is_group_manager"))
                old_manager.user.save()

            form.save()
            manager = form.cleaned_data.get("manager")
            if manager:
                manager.user.user_permissions.add(Permission.objects.get(codename="is_room_manager"))
                manager.user.save()
            return True
        except Group.DoesNotExist:
            return False

    @staticmethod
    def find_all_subgroups(group):
        queryset = Group.objects.filter(parent=group)
        return_queryset = Group.objects.none()
        while True:
            for group_ in queryset:
                return_queryset = queryset | Group.objects.filter(parent=group_) | return_queryset
            for group_ in return_queryset:
                queryset = queryset | Group.objects.filter(parent=group_)
            if list(queryset) == list(return_queryset):
                return return_queryset | Group.objects.filter(id=group.id)


class RoomService:
    @staticmethod
    def find_by_id(room_id):
        try:
            return Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Room.objects.all()

    @staticmethod
    def find_all_public():
        return Room.objects.filter(group=None)

    @staticmethod
    def save(form):
        room = form.save()
        manager = form.cleaned_data.get("manager")
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename="is_room_manager"))
            manager.user.save()
        if not room.group:
            room.locked = False
            room.save()
        return

    @staticmethod
    def delete(room_id, room=None):
        try:
            room = Room.objects.get(pk=room_id) if room is None else room
            manager = room.manager
            if manager:
                managed_rooms = Room.objects.filter(manager=manager)
                if len(managed_rooms) < 2:
                    manager.user.user_permissions.remove(Permission.objects.get(codename="is_room_manager"))
                manager.user.save()
            Room.delete(room)
            return True
        except Room.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(form, old_room):
        try:
            old_manager = old_room.manager
            if old_manager:
                managed_rooms = Room.objects.filter(manager=old_manager)
                if len(managed_rooms) < 2:
                    old_manager.user.user_permissions.remove(Permission.objects.get(codename="is_room_manager"))
                old_manager.user.save()

            room = form.save()
            manager = form.cleaned_data.get("manager")
            if manager:
                manager.user.user_permissions.add(Permission.objects.get(codename="is_room_manager"))
                manager.user.save()
            if not room.group:
                room.locked = False
                room.save()
            return True
        except Room.DoesNotExist:
            return False

    @staticmethod
    def find_all_reservable_rooms(user):
        occupied = RoomService.find_occupied_rooms(user)
        group_set = Person.objects.get(user=user).group_set
        in_group = Room.objects.none()
        for group in group_set.all():
            in_group = in_group | RoomService.find_rooms_for_group(group)
        return occupied | in_group

    @staticmethod
    def find_occupied_rooms(user):
        person = Person.objects.get(user=user)
        return Room.objects.filter(occupies=person)

    @staticmethod
    def find_rooms_for_group(group):
        return Room.objects.filter(group=group)

    @staticmethod
    def find_managed_rooms(user):
        person = Person.objects.get(user=user)
        directly_managed = Room.objects.filter(manager=person)

        managed_groups = Group.objects.filter(manager=person)
        subgroups = Group.objects.none()
        for group in managed_groups:
            subgroups = subgroups | GroupService.find_all_subgroups(group)

        for subgroup in subgroups:
            directly_managed = directly_managed | RoomService.find_rooms_for_group(subgroup)

        return directly_managed


class ReservationStatusService:
    @staticmethod
    def find_by_id(reservation_status_id):
        try:
            return ReservationStatus.objects.get(pk=reservation_status_id)
        except ReservationStatus.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return ReservationStatus.objects.all()

    @staticmethod
    def save(data, user):
        author = Person.objects.get(user=user)
        timestamp = datetime.now()
        reservation_status = ReservationStatus.objects.create(
            author=author, status=data.get("status"), dt_modified=timestamp, note=data.get("note")
        )
        reservation_status.save()
        return reservation_status

    @staticmethod
    def delete(reservation_status_id):
        try:
            ReservationStatus.delete(ReservationStatus.objects.get(pk=reservation_status_id))
            return True
        except ReservationStatus.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(reservation_status_id, updated_reservation_status):
        try:
            ReservationStatus.objects.get(pk=reservation_status_id).update(
                author=updated_reservation_status.author,
                status=updated_reservation_status.status,
                note=updated_reservation_status.note,
            )
            return True
        except ReservationStatus.DoesNotExist:
            return False


class ReservationService:
    @staticmethod
    def find_by_id(reservation_id):
        try:
            return Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Reservation.objects.all()

    @staticmethod
    def save(data, user):
        try:
            author = Person.objects.get(user=user)
            timestamp = datetime.now()
            reservation_status = ReservationStatus.objects.create(
                author=author, dt_modified=timestamp, note=data.get("note")
            )
            reservation_status.save()

            reservation = Reservation.objects.create(
                author=author,
                owner=data.get("owner") if data.get("owner") else author,
                dt_from=data.get("dt_from"),
                dt_to=data.get("dt_to"),
                dt_created=timestamp,
                room=data.get("room"),
            )
            reservation.save()

            reservation.attendees.set(data.get("attendees"))
            reservation.reservation_status.add(reservation_status)
        except IntegrityError:
            return None
        return reservation

    @staticmethod
    def delete(reservation_id):
        try:
            Reservation.delete(Reservation.objects.get(pk=reservation_id))
            return True
        except Reservation.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(reservation, data, user):
        author = Person.objects.get(user=user)
        timestamp = datetime.now()
        reservation_status = ReservationStatus.objects.create(
            author=author, dt_modified=timestamp, note=data.get("note")
        )
        reservation_status.save()

        reservation.author = author
        reservation.owner = data.get("owner")
        reservation.dt_from = data.get("dt_from")
        reservation.dt_to = data.get("dt_to")
        reservation.dt_created = timestamp
        reservation.room = data.get("room")
        reservation.save()

        reservation.attendees.set(data.get("attendees"))
        reservation.reservation_status.add(reservation_status)
        reservation.save()

        return reservation

    @staticmethod
    def add_status(reservation, reservation_status):
        reservation.reservation_status.add(reservation_status)
        return reservation

    @staticmethod
    def find_reservations_for_room(room):
        return Reservation.objects.filter(
            room=room,
            reservation_status__status__exact=ReservationStatus.APPROVED,
            reservation_status__reservation_status__dt_from__lte=datetime.now() + timedelta(days=14),
        )

    @staticmethod
    def find_reservations_for_person(user):
        person = Person.objects.get(user=user)
        return Reservation.objects.filter(owner=person)
