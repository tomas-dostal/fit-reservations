from datetime import datetime, timedelta

from django.db import models
from django.db.utils import IntegrityError

from reservations.models import *
from reservations.services.room_service import RoomService


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
            reservation = Reservation.objects.get(pk=reservation_id)
            for status in reservation.reservation_status.all():
                status.delete()
            Reservation.delete(reservation)
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
            reservation_status__reservation_status__dt_to__gte=datetime.now()
        ).order_by("dt_from")

    @staticmethod
    def find_all_reservations_for_room(room):
        return Reservation.objects.filter(room=room)

    @staticmethod
    def find_reservations_for_person(user):
        person = Person.objects.get(user=user)
        return Reservation.objects.filter(owner=person)

    @staticmethod
    def find_managed_reservations(user):
        managed_rooms = RoomService.find_managed_rooms(user)
        managed_reservations = Reservation.objects.none()

        for room in managed_rooms:
            managed_reservations = managed_reservations | ReservationService.find_all_reservations_for_room(room)

        return managed_reservations
