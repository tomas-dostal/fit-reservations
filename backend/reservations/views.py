from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.template import loader
from django.views import View

from rest_framework import viewsets

from reservations.serializers import *
from reservations.models import *

from reservations.services import *

from reservations.forms import *


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
        template = loader.get_template('persons/detail.html')
        return HttpResponse(template.render({'person': person}, request))

    @staticmethod
    def persons_get_view(request):
        persons = PersonService.find_all()

        template = loader.get_template('persons/list.html')
        return HttpResponse(template.render({'persons': persons}, request))

    @staticmethod
    def person_delete_view(request, person_id):
        if not PersonService.delete(person_id):
            return HttpResponse(template.render({"errors": ["Failed to delete person"]}, request))
        return redirect("/persons/")

    @staticmethod
    def person_create_view(request):
        form = PersonForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/persons/")
        template = loader.get_template('persons/create.html')
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
        template = loader.get_template('persons/create.html')
        return HttpResponse(template.render({'form': form}, request))
