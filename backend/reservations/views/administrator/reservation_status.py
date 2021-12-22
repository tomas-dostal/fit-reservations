from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets

from reservations.models import ReservationStatus
from reservations.serializers import ReservationStatusSerializer
from reservations.services import *
from reservations.forms import ReservationStatusForm
from reservations.models import Reservation
from rest_framework.response import Response


class AdminReservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'trace', ]

    def create(self, request, *args, **kwargs):
        reservation_id = request.data.pop("id")
        status_data = super().create(request, *args, **kwargs).data
        status = ReservationStatus.objects.get(dt_modified=status_data["dt_modified"])
        reservation = Reservation.objects.get(pk=reservation_id)

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

        template = loader.get_template("administrator/reservation_status/create.html")
        form = ReservationStatusForm(request.POST or None)

        if form.is_valid():
            reservation_status = ReservationStatusService.save(form.cleaned_data, request.user)

            ReservationService.add_status(reservation, reservation_status)
            return redirect("/administrator/reservations")
        return HttpResponse(template.render({"form": form}, request))
