from reservations.models import *
from django.db import models
from django.contrib.auth.models import  Permission


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
    def delete(room_id):
        try:
            room = Room.objects.get(pk=room_id)
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
    def update(form, old_room_id):
        try:
            old_manager = Room.objects.get(pk=old_room_id).manager
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
        in_group = Room.objects.none()
        for group in Person.objects.get(user=user).groups.all():
            in_group = in_group | RoomService.find_rooms_for_group(group)
        return (occupied | in_group).distinct()

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

    @staticmethod
    def find_managed_rooms_to_change(user):
        person = Person.objects.get(user=user)
        managed_groups = Group.objects.filter(manager=person)

        subgroups = Group.objects.none()
        for group in managed_groups:
            subgroups = subgroups | GroupService.find_all_subgroups(group)
        managed_rooms = Room.objects.none()
        for subgroup in subgroups:
            managed_rooms = managed_rooms | RoomService.find_rooms_for_group(subgroup)

        return managed_rooms

    @staticmethod
    def set_rooms_group(group, room_ids):
        prev_rooms = Room.objects.filter(group=group)
        prev_rooms.update(group=None)
        rooms = Room.objects.filter(pk__in=room_ids)
        rooms.update(group=group)
        return