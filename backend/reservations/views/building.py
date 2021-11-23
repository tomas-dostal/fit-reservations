from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from rest_framework import viewsets
from ..serializers import BuildingSerializer
from ..models import Building
from ..services import BuildingService
from ..forms import BuildingForm


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class BuildingTemplateView:
    @staticmethod
    def building_get_view(request, building_id):
        building = BuildingService.find_by_id(building_id)
        template = loader.get_template("buildings/detail.html")
        return HttpResponse(template.render({"building": building}, request))

    @staticmethod
    def buildings_get_view(request):
        buildings = BuildingService.find_all()
        template = loader.get_template("buildings/list.html")
        return HttpResponse(template.render({"buildings": buildings}, request))

    @staticmethod
    def building_delete_view(request, building_id):
        template = loader.get_template("buildings/list.html")
        if not BuildingService.delete(building_id):
            return HttpResponse(template.render({"errors": ["Failed to delete building"]}, request))
        return redirect("/buildings/")

    @staticmethod
    def building_create_view(request):
        form = BuildingForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/buildings/")
        template = loader.get_template("buildings/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def building_edit_view(request, building_id):
        instance = BuildingService.find_by_id(building_id)
        if instance is None:
            raise Http404("Building does not exist")
        form = BuildingForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/buildings/")
        template = loader.get_template("buildings/update.html")
        return HttpResponse(template.render({"form": form}, request))
