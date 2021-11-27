from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets

from ..models import ReservationStatus
from ..serializers import ReservationStatusSerializer
from ..services import ReservationStatusService
from ..forms import ReservationStatusForm
from backend.settings import DEFAULT_PAGE_SIZE


class ReservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer


class ReservationStatusTemplateView(ListView):
    @staticmethod
    def reservation_status_get_view(request, reservation_status_id):
        reservation_status = ReservationStatusService.find_by_id(reservation_status_id)
        template = loader.get_template("reservations/test_list.html")
        return HttpResponse(template.render({"test_list": reservation_status}, request))

    @staticmethod
    def reservation_statuses_get_view(request):
        reservation_statuses = ReservationStatusService.find_all()
        template = loader.get_template("reservations/test_list.html")
        return HttpResponse(template.render({"test_list": reservation_statuses}, request))

    def persons_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(ReservationStatusService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            reservation_statuses = paginator.page(page)
        except PageNotAnInteger:
            reservation_statuses = paginator.page(1)
        except EmptyPage:
            reservation_statuses = paginator.page(paginator.num_pages)

        return render(request, "reservation_statuses/list.html", {"reservation_statuses": reservation_statuses})

    @staticmethod
    def reservation_status_delete_view(request, reservation_status_id):
        template = loader.get_template("reservations/test_list.html")
        if not ReservationStatusService.delete(reservation_status_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation status"]}, request))
        return redirect("/reservationstatuses/")

    @staticmethod
    def reservation_status_create_view(request):
        form = ReservationStatusForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/reservationstatuses/")
        template = loader.get_template("reservations/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def reservation_status_edit_view(request, reservation_status_id):
        instance = ReservationStatusService.find_by_id(reservation_status_id)
        if instance is None:
            raise Http404("Reservation status does not exist")
        form = ReservationStatusForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/reservationstatuses/")
        template = loader.get_template("reservations/create.html")
        return HttpResponse(template.render({"form": form}, request))
