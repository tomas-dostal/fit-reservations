from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from django.core.exceptions import PermissionDenied

from reservations.models import Room
from reservations.serializers import RoomSerializer
from reservations.services import RoomService
from reservations.forms import RoomForm
from reservations.settings import DEFAULT_PAGE_SIZE

from reservations.services import ReservationService


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTemplateView(ListView):
    @staticmethod
    def public_room_get_view(request, room_id):
        room = RoomService.find_by_id(room_id)
        reservations = ReservationService.find_reservations_for_room(room)
        # Check if the room is public
        if room and room.group is not None:
            raise PermissionDenied("Not a public room.")
        template = loader.get_template("rooms/detail.html")
        return HttpResponse(template.render({"room": room, "reservations": reservations}, request))

    @staticmethod
    def public_rooms_get_view(request):
        page = request.GET.get("page", 1)

        paginator = Paginator(RoomService.find_all_public(), DEFAULT_PAGE_SIZE)
        try:
            rooms = paginator.page(page)
        except PageNotAnInteger:
            rooms = paginator.page(1)
        except EmptyPage:
            rooms = paginator.page(paginator.num_pages)

        return render(request, "rooms/public_list.html", {"rooms": rooms})
