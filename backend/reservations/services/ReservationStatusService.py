from datetime import datetime
from reservations.models import *
from django.db import models


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