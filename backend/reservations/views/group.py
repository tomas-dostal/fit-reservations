from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from ..serializers import GroupSerializer
from ..models import Group
from ..services import GroupService
from ..forms import GroupForm
from backend.settings import DEFAULT_PAGE_SIZE


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupTemplateView(ListView):
    @staticmethod
    def group_get_view(request, group_id):
        group = GroupService.find_by_id(group_id)
        template = loader.get_template("groups/detail.html")
        return HttpResponse(template.render({"group": group}, request))

    @staticmethod
    def groups_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(GroupService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            groups = paginator.page(page)
        except PageNotAnInteger:
            groups = paginator.page(1)
        except EmptyPage:
            groups = paginator.page(paginator.num_pages)

        return render(request, "groups/list.html", {"groups": groups})

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
