from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from rest_framework.response import Response

from reservations.decorators import user_passes_test
from reservations.forms import ReservationStatusForm
from reservations.models import Reservation
from reservations.permissions import AdminPermission
from reservations.permissions import ReservationStatusPermission
from reservations.serializers import ReservationStatusSerializer
from reservations.services import *
from reservations.services import ReservationService
from reservations.services import RoomService


class AdminReservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "trace",
    ]
    permission_classes = [AdminPermission]

    def get_permissions(self):
        if self.action == "create":
            return [ReservationStatusPermission()]
        return super(AdminReservationStatusViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        if "id" in request.data:
            reservation_id = request.data.pop("id")
        else:
            return Response(data="Reservation id missing", status=400)
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return Response(data="Reservation not found", status=404)
        managed_reservations = ReservationService.find_managed_reservations(request.user)

        if reservation not in managed_reservations.all() and not request.user.is_superuser:
            return Response(data="Cant manage this reservation", status=403)

        status_data = super().create(request, *args, **kwargs).data
        status = ReservationStatus.objects.get(dt_modified=status_data["dt_modified"])

        reservation.reservation_status.add(status)
        reservation.save()
        return Response(status_data)

    def get_serializer_context(self):
        return {"request": self.request}


class AdminReservationStatusTemplateView(ListView):
    @staticmethod
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_room_manager")
        or u.has_perm("reservations.is_group_manager")
    )
    def status_create_view(request, reservation_id):
        reservation = ReservationService.find_by_id(reservation_id)
        if not reservation:
            raise Http404("Reservation does not exist")
        if reservation.room not in RoomService.find_managed_rooms(request.user) and not request.user.is_superuser:
            raise PermissionDenied

        template = loader.get_template("administrator/reservation_status/create.html")
        form = ReservationStatusForm(request.POST or None)

        if form.is_valid():
            reservation_status = ReservationStatusService.save(form.cleaned_data, request.user)

            ReservationService.add_status(reservation, reservation_status)
            return redirect("/administrator/reservations")
        return HttpResponse(template.render({"form": form}, request))
