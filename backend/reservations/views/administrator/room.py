from datetime import datetime
from pytz import timezone
from django.contrib.auth.models import Permission
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from django.contrib.auth.decorators import user_passes_test
from reservations.models import Room
from reservations.serializers import RoomSerializer
from reservations.services import RoomService
from reservations.forms import RoomForm, RoomGroupManagerForm
from backend.settings import DEFAULT_PAGE_SIZE
from rest_framework.decorators import action
from rest_framework.response import Response
from reservations.models import Person
from reservations.services import ReservationService
from reservations.models import ReservationStatus
from reservations.services import PersonService
from reservations.permissions import RoomPermission


class AdminRoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'put', 'head', 'options', 'trace', ]
    permission_classes = [RoomPermission]

    def get_permissions(self):
        if self.action == 'lock' or self.action == 'access':
            return []
        return super(AdminRoomViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Room.objects.all()
        return RoomService.find_managed_rooms(self.request.user)

    def destroy(self, request, *args, **kwargs):
        RoomService.delete(self.get_object().id)
        return Response(data='delete success')

    def create(self, request, *args, **kwargs):
        manager = Person.objects.get(pk=request.data["manager"])
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename="is_room_manager"))
            manager.user.save()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        old_manager = Person.objects.get(pk=self.get_object().manager.id)
        if old_manager:
            managed_rooms = Room.objects.filter(manager=old_manager)
            if len(managed_rooms) < 2:
                old_manager.user.user_permissions.remove(Permission.objects.get(codename="is_room_manager"))
            old_manager.user.save()

        new_manager = Person.objects.get(pk=request.data["manager"])
        if new_manager:
            new_manager.user.user_permissions.add(Permission.objects.get(codename="is_room_manager"))
            new_manager.user.save()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if 'manager' not in request.data:
            return Response(data='Manager to change not specified', status=400)
        kwargs['partial'] = True
        request._full_data = {
            'manager': request.data['manager']
        }
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def lock(self, request, pk):
        room = RoomService.find_by_id(pk)

        if request.user.is_superuser:
            room.locked = not room.locked
            room.save()
            return Response(data='Locking or unlocking successful')

        reservations = ReservationService.find_reservations_for_person(request.user)

        for reservation in reservations:
            if reservation.room == room:
                if reservation.dt_from < datetime.now(timezone('Europe/Berlin')) < reservation.dt_to:
                    room.locked = not room.locked
                    room.save()
                    return Response(data='Locking or unlocking successful')

        return Response(data='Cant lock or unlock this room', status=403)

    @action(detail=True, methods=['GET'])
    def access(self, request, pk):
        room = RoomService.find_by_id(pk)
        person = Person.objects.get(user=request.user)

        if request.user.is_superuser or not room.locked or room in person.occupy.all():
            return Response(data='Access granted')

        reservations = ReservationService.find_reservations_for_room(room)

        for reservation in reservations:
            if reservation.dt_from < datetime.now(timezone('Europe/Berlin')) < reservation.dt_to and \
                    reservation.reservation_status.last().status == ReservationStatus.APPROVED:
                if person in reservation.attendees.all() or person == reservation.owner:
                    return Response(data='Access granted')
        return Response(data='Access denied')


class AdminRoomTemplateView(ListView):
    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def room_get_view(request, room_id):
        room = RoomService.find_by_id(room_id)
        template = loader.get_template("administrator/rooms/detail.html")
        return HttpResponse(template.render({"room": room}, request))

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser or u.has_perm("reservations.is_group_manager"))
    def rooms_get_view(request):
        page = request.GET.get("page", 1)
        if request.user.is_superuser:
            paginator = Paginator(RoomService.find_all(), DEFAULT_PAGE_SIZE)
        else:
            paginator = Paginator(RoomService.find_managed_rooms_to_change(request.user), DEFAULT_PAGE_SIZE)

        try:
            rooms = paginator.page(page)
        except PageNotAnInteger:
            rooms = paginator.page(1)
        except EmptyPage:
            rooms = paginator.page(paginator.num_pages)

        return render(request, "administrator/rooms/list.html", {"rooms": rooms})

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def room_delete_view(request, room_id):
        template = loader.get_template("administrator/rooms/list.html")
        if not RoomService.delete(room_id):
            return HttpResponse(template.render({"errors": ["Failed to delete room"]}, request))
        return redirect("/administrator/rooms/")

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def room_create_view(request):
        form = RoomForm(request.POST or None)
        if form.is_valid():
            RoomService.save(form)
            return redirect("/administrator/rooms/")
        template = loader.get_template("administrator/rooms/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser or u.has_perm("reservations.is_group_manager"))
    def room_edit_view(request, room_id):
        if request.user.is_superuser:
            instance = RoomService.find_by_id(room_id)
            if instance is None:
                raise Http404("Room does not exist")
            form = RoomForm(request.POST or None, instance=instance)
            if form.is_valid():
                RoomService.update(form, room_id)
                return redirect("/administrator/rooms/")
            template = loader.get_template("administrator/rooms/update.html")
            return HttpResponse(template.render({"form": form}, request))

        instance = RoomService.find_by_id(room_id)
        if instance is None:
            raise Http404("Room does not exist")
        form = RoomGroupManagerForm(request.POST or None, instance=instance)
        if form.is_valid():
            RoomService.update(form, room_id)
            return redirect("/administrator/rooms/")
        template = loader.get_template("administrator/rooms/update_manager.html")
        return HttpResponse(template.render({"form": form}, request))
