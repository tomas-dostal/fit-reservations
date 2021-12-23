from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.models import Permission
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from reservations.serializers import GroupSerializer
from reservations.models import Group
from reservations.services import GroupService
from reservations.forms import GroupForm
from backend.settings import DEFAULT_PAGE_SIZE
from rest_framework.response import Response
from reservations.models import Person
from reservations.permissions import AdminPermission


class AdminGroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'delete', 'put', 'head', 'options', 'trace', ]
    permission_classes = [AdminPermission]

    def destroy(self, request, *args, **kwargs):
        GroupService.delete(self.get_object().id)
        return Response(data='delete success')

    def create(self, request, *args, **kwargs):
        manager = Person.objects.get(pk=request.data["manager"])
        if manager:
            manager.user.user_permissions.add(Permission.objects.get(codename="is_group_manager"))
            manager.user.save()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        old_manager = Person.objects.get(pk=self.get_object().manager.id)
        if old_manager:
            managed_groups = Group.objects.filter(manager=old_manager)
            if len(managed_groups) < 2:
                old_manager.user.user_permissions.remove(Permission.objects.get(codename="is_group_manager"))
            old_manager.user.save()

        new_manager = Person.objects.get(pk=request.data["manager"])
        if new_manager:
            new_manager.user.user_permissions.add(Permission.objects.get(codename="is_group_manager"))
            new_manager.user.save()
        return super().update(request, *args, **kwargs)


class AdminGroupTemplateView(ListView):
    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def group_get_view(request, group_id):
        group = GroupService.find_by_id(group_id)
        template = loader.get_template("administrator/groups/detail.html")
        return HttpResponse(template.render({"group": group}, request))

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def groups_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(GroupService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        return render(request, "administrator/groups/list.html", {"groups": groups})

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def group_delete_view(request, group_id):
        template = loader.get_template("administrator/groups/list.html")
        if not GroupService.delete(group_id):
            return HttpResponse(template.render({"errors": ["Failed to delete group"]}, request))
        return redirect("/administrator/groups/")

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def group_create_view(request):
        form = GroupForm(request.POST or None)
        if form.is_valid():
            GroupService.save(form)
            return redirect("/administrator/groups/")
        template = loader.get_template("administrator/groups/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    @user_passes_test(lambda u: u.is_superuser)
    def group_edit_view(request, group_id):
        instance = GroupService.find_by_id(group_id)
        if instance is None:
            raise Http404("Building does not exist")
        form = GroupForm(request.POST or None, instance=instance)
        if form.is_valid():
            GroupService.update(form, group_id)
            return redirect("/administrator/groups/")
        template = loader.get_template("administrator/groups/update.html")
        return HttpResponse(template.render({"form": form}, request))
