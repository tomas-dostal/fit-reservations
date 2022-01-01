from rest_framework import permissions

from reservations.services import ReservationService
from reservations.services import RoomService


class RoomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET" or request.method == "PATCH":
            return request.user.has_perm("reservations.is_group_manager") or request.user.is_superuser
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        managed_rooms = RoomService.find_managed_rooms_to_change(request.user)
        room = RoomService.find_by_id(obj.id)

        if room in managed_rooms.all():
            return True
        return False


class ReservationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.has_perm("reservations.is_group_manager")
            or request.user.has_perm("reservations.is_room_manager")
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        managed_reservations = ReservationService.find_managed_reservations(request.user)
        reservation = ReservationService.find_by_id(obj.id)

        if reservation in managed_reservations.all():
            return True
        return False


class ReservationStatusPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.has_perm("reservations.is_group_manager")
            or request.user.has_perm("reservations.is_room_manager")
        )


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
