from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from rest_framework import viewsets

from ..models import Room
from ..serializers import RoomSerializer
from ..services import RoomService
from ..forms import RoomForm


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTemplateView:
    @staticmethod
    def room_get_view(request, room_id):
        room = RoomService.find_by_id(room_id)
        template = loader.get_template("rooms/detail.html")
        return HttpResponse(template.render({"room": room}, request))

    @staticmethod
    def rooms_get_view(request):
        rooms = RoomService.find_all()
        template = loader.get_template("rooms/list.html")
        return HttpResponse(template.render({"rooms": rooms}, request))

    @staticmethod
    def room_delete_view(request, room_id):
        template = loader.get_template("rooms/list.html")
        if not RoomService.delete(room_id):
            return HttpResponse(template.render({"errors": ["Failed to delete room"]}, request))
        return redirect("/rooms/")

    @staticmethod
    def room_create_view(request):
        form = RoomForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/rooms/")
        template = loader.get_template("rooms/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def room_edit_view(request, room_id):
        instance = RoomService.find_by_id(room_id)
        if instance is None:
            raise Http404("Room does not exist")
        form = RoomForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/rooms/")
        template = loader.get_template("rooms/update.html")
        return HttpResponse(template.render({"form": form}, request))
