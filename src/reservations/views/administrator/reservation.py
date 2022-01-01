from reservations.decorators import user_passes_test
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from reservations.forms import AdminReservationForm
from reservations.serializers import *
from reservations.services import *
from reservations.settings import DEFAULT_PAGE_SIZE
from reservations.models import Person
from reservations.models import ReservationStatus
from reservations.models import Reservation
from rest_framework.response import Response
from reservations.services import ReservationService
from reservations.permissions import ReservationPermission


class AdminReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "put",
        "head",
        "options",
        "trace",
    ]
    permission_classes = [ReservationPermission]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Reservation.objects.all()
        return ReservationService.find_managed_reservations(self.request.user)

    def destroy(self, request, *args, **kwargs):
        ReservationService.delete(self.get_object().id)
        return Response(data="delete success")

    def create(self, request, *args, **kwargs):
        author = Person.objects.get(user=request.user)
        reservation_status = ReservationStatus.objects.create(
            author=author, note=request.data["note"] if "note" in request.data else "Reservation"
        )
        request.data["author"] = author.id
        reservation_data = super().create(request, *args, **kwargs).data
        reservation_data["reservation_status"] = [reservation_status.id]
        reservation = Reservation.objects.get(dt_created=reservation_data["dt_created"])
        reservation.reservation_status.add(reservation_status)
        reservation.save()
        return Response(reservation_data)

    def update(self, request, *args, **kwargs):
        author = Person.objects.get(user=request.user)
        reservation_status = ReservationStatus.objects.create(
            author=author, note=request.data["note"] if "note" in request.data else "Reservation"
        )
        request.data["author"] = author.id
        reservation_data = super().update(request, *args, **kwargs).data
        reservation = self.get_object()
        reservation.reservation_status.add(reservation_status)
        reservation.save()

        reservation_data["reservation_status"] = [status.id for status in reservation.reservation_status.all()]
        return Response(reservation_data)

    def partial_update(self, request, *args, **kwargs):
        if "attendees" not in request.data:
            return Response(data="Attendees to change not specified", status=400)
        kwargs["partial"] = True
        request._full_data = {"attendees": request.data["attendees"]}
        return self.update(request, *args, **kwargs)

    def get_serializer_context(self):
        return {"request": self.request}


class AdminReservationTemplateView(ListView):
    @staticmethod
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_room_manager")
        or u.has_perm("reservations.is_group_manager")
    )
    def reservation_get_view(request, reservation_id):
        reservation = ReservationService.find_by_id(reservation_id)
        template = loader.get_template("administrator/reservations/detail.html")
        return HttpResponse(template.render({"reservation": reservation}, request))

    @staticmethod
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_room_manager")
        or u.has_perm("reservations.is_group_manager")
    )
    def reservations_get_view(request):
        page = request.GET.get("page", 1)

        if request.user.is_superuser:
            paginator = Paginator(ReservationService.find_all(), DEFAULT_PAGE_SIZE)
        else:
            paginator = Paginator(ReservationService.find_managed_reservations(request.user), DEFAULT_PAGE_SIZE)

        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)

        return render(request, "administrator/reservations/list.html", {"reservations": reservations})

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def reservation_delete_view(request, reservation_id):
        template = loader.get_template("administrator/reservations/list.html")
        if not ReservationService.delete(reservation_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation"]}, request))
        return redirect("/administrator/reservations/")

    @staticmethod
    @user_passes_test(
        lambda u: u.is_superuser
        or u.has_perm("reservations.is_room_manager")
        or u.has_perm("reservations.is_group_manager")
    )
    def reservation_create_view(request):
        form = AdminReservationForm(request, request.POST or None)
        template = loader.get_template("administrator/reservations/create.html")

        if form.is_valid():
            if not ReservationService.save(form.cleaned_data, request.user):
                return HttpResponse(template.render({"errors": ["Something went wrong"], "form": form}, request))
            return redirect("/administrator/reservations/")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def reservation_edit_view(request, reservation_id):
        instance = ReservationService.find_by_id(reservation_id)
        template = loader.get_template("administrator/reservations/update.html")

        if instance is None:
            raise Http404("Reservation does not exist")
        form = AdminReservationForm(request, request.POST or None, instance=instance)

        if form.is_valid():
            if not ReservationService.update(form.cleaned_data):
                return HttpResponse(template.render({"errors": ["Something went wrong"], "form": form}, request))
            return redirect("/administrator/reservations/")
        return HttpResponse(template.render({"form": form, "reservation": instance}, request))
