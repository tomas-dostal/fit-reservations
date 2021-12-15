from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from reservations.forms import ReservationForm
from reservations.serializers import *
from reservations.services import *
from datetime import datetime
from backend.settings import DEFAULT_PAGE_SIZE


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationTemplateView(ListView):
    @staticmethod
    def reservation_get_view(request, reservation_id):
        reservation = ReservationService.find_by_id(reservation_id)
        template = loader.get_template("reservations/detail.html")
        return HttpResponse(template.render({"reservation": reservation}, request))

    @staticmethod
    def reservations_get_view(request):
        page = request.GET.get("page", 1)
        paginator = Paginator(ReservationService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)

        return render(request, "reservations/publiclist.html", {"reservations": reservations})

    @staticmethod
    def reservation_delete_view(request, reservation_id):
        template = loader.get_template("reservations/publiclist.html")
        if not ReservationService.delete(reservation_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation"]}, request))
        return redirect("/reservations/")

    @staticmethod
    def reservation_create_view(request):
        form = ReservationForm(request, request.POST or None)
        template = loader.get_template("reservations/create.html")

        if form.is_valid():
            if not ReservationService.save(form.cleaned_data, request.user):
                return HttpResponse(template.render({"errors": ["Something went wrong"], "form": form}, request))
            return redirect("/")
        return HttpResponse(template.render({"form": form}, request))
