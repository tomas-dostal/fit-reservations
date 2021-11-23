from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from rest_framework import viewsets
from ..serializers import GroupSerializer
from ..models import Group
from ..services import GroupService
from ..forms import GroupForm


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupTemplateView:
    @staticmethod
    def group_get_view(request, group_id):
        group = GroupService.find_by_id(group_id)
        template = loader.get_template("groups/detail.html")
        return HttpResponse(template.render({"group": group}, request))

    @staticmethod
    def groups_get_view(request):
        groups = GroupService.find_all()
        template = loader.get_template("groups/list.html")
        return HttpResponse(template.render({"groups": groups}, request))

    @staticmethod
    def group_delete_view(request, group_id):
        template = loader.get_template("groups/list.html")
        if not GroupService.delete(group_id):
            return HttpResponse(template.render({"errors": ["Failed to delete group"]}, request))
        return redirect("/groups/")

    @staticmethod
    def group_create_view(request):
        form = GroupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/groups/")
        template = loader.get_template("groups/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def group_edit_view(request, group_id):
        instance = GroupService.find_by_id(group_id)
        if instance is None:
            raise Http404("Building does not exist")
        form = GroupForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/groups/")
        template = loader.get_template("groups/update.html")
        return HttpResponse(template.render({"form": form}, request))
