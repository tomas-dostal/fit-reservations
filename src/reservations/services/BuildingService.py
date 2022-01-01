from reservations.models import *
from django.db import models


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
