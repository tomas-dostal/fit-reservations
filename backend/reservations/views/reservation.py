from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from rest_framework import viewsets

from ..forms import ReservationForm
from ..serializers import *
from ..services import *
from datetime import datetime


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationTemplateView:
    @staticmethod
    def reservation_get_view(request, reservation_id):
        reservation = ReservationService.find_by_id(reservation_id)
        template = loader.get_template("reservations/test_list.html")
        return HttpResponse(template.render({"test_list": reservation}, request))

    @staticmethod
    def reservations_get_view(request):
        reservations = ReservationService.find_all()
        template = loader.get_template("reservations/test_list.html")
        return HttpResponse(template.render({"test_list": reservations}, request))

    @staticmethod
    def reservation_delete_view(request, reservation_id):
        template = loader.get_template("reservations/test_list.html")
        if not ReservationService.delete(reservation_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation"]}, request))
        return redirect("/reservations/")

    @staticmethod
    def reservation_create_view(request):
        form = ReservationForm(request.POST or None)
        if form.is_valid():
            timestamp = datetime.now()
            reservation_status = ReservationStatus()
            reservation_status.author = form.cleaned_data.get("author")
            reservation_status.modified = timestamp
            reservation_status.note = form.cleaned_data.get("note")
            reservation_status.save()

            reservation = Reservation()
            reservation.author = form.cleaned_data.get("author")
            reservation.dt_from = form.cleaned_data.get("dt_from")
            reservation.dt_to = form.cleaned_data.get("dt_to")
            reservation.dt_to = form.cleaned_data.get("dt_to")
            reservation.dt_created = timestamp
            reservation.room = form.cleaned_data.get("room")
            reservation.save()
            reservation.attendees.set(form.cleaned_data.get("attendees"))
            reservation.reservation_status.add(reservation_status)
            return redirect("/reservations/")
        template = loader.get_template("reservations/test_create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def reservation_edit_view(request, reservation_id):
        instance = ReservationService.find_by_id(reservation_id)
        if instance is None:
            raise Http404("Reservation does not exist")
        form = ReservationForm(request.POST or None, instance=instance)
        if form.is_valid():
            timestamp = datetime.now()
            reservation_status = ReservationStatus()
            reservation_status.author = form.cleaned_data.get("author")
            reservation_status.modified = timestamp
            reservation_status.note = form.cleaned_data.get("note")
            reservation_status.save()

            instance.attendees.set(form.cleaned_data.get("attendees"))
            instance.reservation_status.add(reservation_status)

            form.save()
            return redirect("/reservations/")
        template = loader.get_template("reservations/test_create.html")
        return HttpResponse(template.render({"form": form}, request))
