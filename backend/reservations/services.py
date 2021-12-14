from datetime import datetime

from .models import *
from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.utils import IntegrityError

# TODO Vytvorit metody pro ziskani mistnosti, kde dany uzivatel muze rezervovat


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
            manager.user.user_permissions.add(Permission.objects.get(codename='is_group_manager'))
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
                    manager.user.user_permissions.remove(Permission.objects.get(codename='is_group_manager'))
                manager.user.save()
            Room.delete(group)
            return True
        except Group.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(form):
        try:
            form.save()
            manager = form.cleaned_data.get("manager")
            if manager:
                manager.user.user_permissions.add(Permission.objects.get(codename='is_room_manager'))
                manager.user.save()
            return True
        except Group.DoesNotExist:
            return False


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
    def save(form):
        form.save()
        manager = form.cleaned_data.get("manager")
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename='is_room_manager'))
            manager.user.save()
        return

    @staticmethod
    def delete(room_id):
        try:
            room = Room.objects.get(pk=room_id)
            manager = room.manager
            if manager:
                managed_rooms = Room.objects.filter(manager=manager)
                if len(managed_rooms) < 2:
                    manager.user.user_permissions.remove(Permission.objects.get(codename='is_room_manager'))
                manager.user.save()
            Room.delete(room)
            return True
        except Room.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(form):
        try:
            form.save()
            manager = form.cleaned_data.get("manager")
            if manager:
                manager.user.user_permissions.add(Permission.objects.get(codename='is_room_manager'))
                manager.user.save()
            return True
        except Room.DoesNotExist:
            return False


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
    def save(data):
        timestamp = datetime.now()
        reservation_status = ReservationStatus.objects.create(
            author=data.get("author"), status=data.get("status"), dt_modified=timestamp, note=data.get("note")
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
    def save(data):
        try:
            timestamp = datetime.now()
            reservation_status = ReservationStatus.objects.create(
                author=data.get("author"), dt_modified=timestamp, note=data.get("note")
            )
            reservation_status.save()

            reservation = Reservation.objects.create(
                # TODO Az bude fungovat prihlaseni, mozna predavat metode save rovnou uzivatele, ktery bude author?
                author=data.get("author"),
                owner=data.get("author"),
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
    def update(reservation, data):
        timestamp = datetime.now()
        reservation_status = ReservationStatus.objects.create(
            author=data.get("author"), dt_modified=timestamp, note=data.get("note")
        )
        reservation_status.save()

        reservation.author = (data.get("author"),)
        reservation.owner = (data.get("author"),)
        reservation.dt_from = (data.get("dt_from"),)
        reservation.dt_to = (data.get("dt_to"),)
        reservation.dt_created = (timestamp,)
        reservation.room = data.get("room")
        reservation.save()

        reservation.attendees.set(data.get("attendees"))
        reservation.reservation_status.add(reservation_status)

        return reservation

    @staticmethod
    def add_status(reservation, reservation_status):
        reservation.reservation_status.add(reservation_status)
        return reservation
