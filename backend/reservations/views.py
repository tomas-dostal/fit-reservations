from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import viewsets
from reservations.serializers import *
from reservations.models import *
from reservations.services import *
from reservations.forms import *
from datetime import datetime


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReservationStatusViewSet(viewsets.ModelViewSet):
    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class PersonTemplateView:
    @staticmethod
    def person_get_view(request, person_id):
        person = PersonService.find_by_id(person_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': person}, request))

    @staticmethod
    def persons_get_view(request):
        persons = PersonService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': persons}, request))

    @staticmethod
    def person_delete_view(request, person_id):
        template = loader.get_template('reservations/test_list.html')
        if not PersonService.delete(person_id):
            return HttpResponse(template.render({"errors": ["Failed to delete person"]}, request))
        return redirect("/persons/")

    @staticmethod
    def person_create_view(request):
        form = PersonForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/persons/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def person_edit_view(request, person_id):
        instance = PersonService.find_by_id(person_id)
        if instance is None:
            raise Http404("Person does not exist")
        form = PersonForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/persons/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))


class BuildingTemplateView:
    @staticmethod
    def building_get_view(request, building_id):
        building = BuildingService.find_by_id(building_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': building}, request))

    @staticmethod
    def buildings_get_view(request):
        buildings = BuildingService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': buildings}, request))

    @staticmethod
    def building_delete_view(request, building_id):
        template = loader.get_template('reservations/test_list.html')
        if not BuildingService.delete(building_id):
            return HttpResponse(template.render({"errors": ["Failed to delete building"]}, request))
        return redirect("/buildings/")

    @staticmethod
    def building_create_view(request):
        form = BuildingForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/buildings/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def building_edit_view(request, building_id):
        instance = BuildingService.find_by_id(building_id)
        if instance is None:
            raise Http404("Building does not exist")
        form = BuildingForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/buildings/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))


class GroupTemplateView:
    @staticmethod
    def group_get_view(request, group_id):
        group = GroupService.find_by_id(group_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': group}, request))

    @staticmethod
    def groups_get_view(request):
        groups = GroupService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': groups}, request))

    @staticmethod
    def group_delete_view(request, group_id):
        template = loader.get_template('reservations/test_list.html')
        if not GroupService.delete(group_id):
            return HttpResponse(template.render({"errors": ["Failed to delete group"]}, request))
        return redirect("/groups/")

    @staticmethod
    def group_create_view(request):
        form = GroupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/groups/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def group_edit_view(request, group_id):
        instance = GroupService.find_by_id(group_id)
        if instance is None:
            raise Http404("Building does not exist")
        form = GroupForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/groups/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))


class RoomTemplateView:
    @staticmethod
    def room_get_view(request, room_id):
        room = RoomService.find_by_id(room_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': room}, request))

    @staticmethod
    def rooms_get_view(request):
        rooms = RoomService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': rooms}, request))

    @staticmethod
    def room_delete_view(request, room_id):
        template = loader.get_template('reservations/test_list.html')
        if not RoomService.delete(room_id):
            return HttpResponse(template.render({"errors": ["Failed to delete room"]}, request))
        return redirect("/rooms/")

    @staticmethod
    def room_create_view(request):
        form = RoomForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/rooms/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def room_edit_view(request, room_id):
        instance = RoomService.find_by_id(room_id)
        if instance is None:
            raise Http404("Room does not exist")
        form = RoomForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/rooms/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))


class ReservationStatusTemplateView:
    @staticmethod
    def reservation_status_get_view(request, reservation_status_id):
        reservation_status = ReservationStatusService.find_by_id(reservation_status_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': reservation_status}, request))

    @staticmethod
    def reservation_statuses_get_view(request):
        reservation_statuses = ReservationStatusService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': reservation_statuses}, request))

    @staticmethod
    def reservation_status_delete_view(request, reservation_status_id):
        template = loader.get_template('reservations/test_list.html')
        if not ReservationStatusService.delete(reservation_status_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation status"]}, request))
        return redirect("/reservationstatuses/")

    @staticmethod
    def reservation_status_create_view(request):
        form = ReservationStatusForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/reservationstatuses/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def reservation_status_edit_view(request, reservation_status_id):
        instance = ReservationStatusService.find_by_id(reservation_status_id)
        if instance is None:
            raise Http404("Reservation status does not exist")
        form = ReservationStatusForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/reservationstatuses/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))


class ReservationTemplateView:
    @staticmethod
    def reservation_get_view(request, reservation_id):
        reservation = ReservationService.find_by_id(reservation_id)
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': reservation}, request))

    @staticmethod
    def reservations_get_view(request):
        reservations = ReservationService.find_all()
        template = loader.get_template('reservations/test_list.html')
        return HttpResponse(template.render({'test_list': reservations}, request))

    @staticmethod
    def reservation_delete_view(request, reservation_id):
        template = loader.get_template('reservations/test_list.html')
        if not ReservationService.delete(reservation_id):
            return HttpResponse(template.render({"errors": ["Failed to delete reservation"]}, request))
        return redirect("/reservations/")

    @staticmethod
    def reservation_create_view(request):
        form = ReservationForm(request.POST or None)
        if form.is_valid():
            timestamp = datetime.now()
            reservation_status = ReservationStatus()
            reservation_status.author = form.cleaned_data.get('author')
            reservation_status.modified = timestamp
            reservation_status.note = form.cleaned_data.get('note')
            reservation_status.save()

            reservation = Reservation()
            reservation.author = form.cleaned_data.get('author')
            reservation.dt_from = form.cleaned_data.get('dt_from')
            reservation.dt_to = form.cleaned_data.get('dt_to')
            reservation.dt_to = form.cleaned_data.get('dt_to')
            reservation.dt_created = timestamp
            reservation.room = form.cleaned_data.get('room')
            reservation.save()
            reservation.attendees.set(form.cleaned_data.get('attendees'))
            reservation.reservation_status.set([reservation_status])
            return redirect("/reservations/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))

    @staticmethod
    def reservation_edit_view(request, reservation_id):
        instance = ReservationService.find_by_id(reservation_id)
        if instance is None:
            raise Http404("Reservation does not exist")
        form = ReservationForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/reservations/")
        template = loader.get_template('reservations/test_create.html')
        return HttpResponse(template.render({'form': form}, request))