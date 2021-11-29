from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets

from ..models import Room
from ..serializers import RoomSerializer
from ..services import RoomService
from ..forms import RoomForm
from backend.settings import DEFAULT_PAGE_SIZE


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomTemplateView(ListView):
    @staticmethod
    def room_get_view(request, room_id):
        room = RoomService.find_by_id(room_id)
        template = loader.get_template("administrator/rooms/detail.html")
        return HttpResponse(template.render({"room": room}, request))

    @staticmethod
    def rooms_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(RoomService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            rooms = paginator.page(page)
        except PageNotAnInteger:
            rooms = paginator.page(1)
        except EmptyPage:
            rooms = paginator.page(paginator.num_pages)

        return render(request, "administrator/rooms/list.html", {"rooms": rooms})

    @staticmethod
    def room_delete_view(request, room_id):
        template = loader.get_template("administrator/rooms/list.html")
        if not RoomService.delete(room_id):
            return HttpResponse(template.render({"errors": ["Failed to delete room"]}, request))
        return redirect("/rooms/")

    @staticmethod
    def room_create_view(request):
        form = RoomForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/rooms/")
        template = loader.get_template("administrator/rooms/create.html")
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
        template = loader.get_template("administrator/rooms/update.html")
        return HttpResponse(template.render({"form": form}, request))
