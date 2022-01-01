from django.contrib.auth.models import Permission
from django.db import models

from reservations.models import *


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
        instance = form.save()
        manager = form.cleaned_data.get("manager")
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename="is_group_manager"))
            manager.user.save()
        RoomService.set_rooms_group(instance, [room.id for room in form.cleaned_data.get("rooms")])
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

            rooms = RoomService.find_rooms_for_group(group)

            for room in rooms:
                RoomService.delete(room.id)

            Group.delete(group)
            return True
        except Group.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(form, old_group_id):
        try:
            old_manager = Group.objects.get(pk=old_group_id).manager
            if old_manager:
                managed_groups = Group.objects.filter(manager=old_manager)
                if len(managed_groups) < 2:
                    old_manager.user.user_permissions.remove(Permission.objects.get(codename="is_group_manager"))
                old_manager.user.save()

            instance = form.save()
            manager = form.cleaned_data.get("manager")
            if manager:
                manager.user.user_permissions.add(Permission.objects.get(codename="is_group_manager"))
                manager.user.save()
            RoomService.set_rooms_group(instance, [room.id for room in form.cleaned_data.get("rooms")])
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
