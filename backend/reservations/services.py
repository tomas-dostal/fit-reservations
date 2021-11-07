from .models import *
from django.db import models


class UserService:

    @staticmethod
    def find_by_id(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return User.objects.all()

    @staticmethod
    def save(user):
        user.save()
        return

    @staticmethod
    def delete(user):
        try:
            User.delete(User.objects.get(pk=user.id))
            return True
        except User.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(user_id, updated_user):
        try:
            User.objects.get(pk=user_id).update(
                name=updated_user.name,
                surname=updated_user.surname,
                is_admin=updated_user.is_admin
            )
            return True
        except User.DoesNotExist:
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
    def delete(building):
        try:
            Building.delete(Building.objects.get(pk=building.id))
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
    def save(group):
        group.save()
        return

    @staticmethod
    def delete(group):
        try:
            Group.delete(Group.objects.get(pk=group.id))
            return True
        except Group.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(group_id, updated_group):
        try:
            Group.objects.get(pk=group_id).update(
                name=updated_group.name,
                manager=updated_group.manager,
                subgroup=updated_group.subgroup
            )
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
    def save(room):
        room.save()
        return

    @staticmethod
    def delete(room):
        try:
            Room.delete(Room.objects.get(pk=room.id))
            return True
        except Room.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(room_id, updated_room):
        try:
            Room.objects.get(pk=room_id).update(
                name=updated_room.name,
                manager=updated_room.manager,
                group=updated_room.group,
                building=updated_room.building
            )
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
    def save(reservation_status):
        reservation_status.save()
        return

    @staticmethod
    def delete(reservation_status):
        try:
            ReservationStatus.delete(ReservationStatus.objects.get(pk=reservation_status.id))
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
                note=updated_reservation_status.note
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
    def save(reservation):
        reservation.save()
        return

    @staticmethod
    def delete(reservation):
        try:
            Reservation.delete(Reservation.objects.get(pk=reservation.id))
            return True
        except Reservation.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(reservation_id, updated_reservation):
        try:
            Reservation.objects.get(pk=reservation_id).update(
                author=updated_reservation.author,
                attendees=updated_reservation.attendees,
                room=updated_reservation.room,
                reservation_status=updated_reservation.reservation_status,
                dt_from=updated_reservation.dt_from,
                dt_to=updated_reservation.dt_to,
                dt_created=updated_reservation.dt_created
            )
            return True
        except Reservation.DoesNotExist:
            return False
