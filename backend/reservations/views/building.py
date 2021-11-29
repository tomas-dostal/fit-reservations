from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from ..serializers import BuildingSerializer
from ..models import Building
from ..services import BuildingService
from ..forms import BuildingForm
from backend.settings import DEFAULT_PAGE_SIZE


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class BuildingTemplateView(ListView):
    paginate_by = 10
    context_object_name = "building-list"

    @staticmethod
    def building_get_view(request, building_id):
        building = BuildingService.find_by_id(building_id)
        template = loader.get_template("administrator/buildings/detail.html")
        return HttpResponse(template.render({"building": building}, request))

    @staticmethod
    def buildings_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(BuildingService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            buildings = paginator.page(page)
        except PageNotAnInteger:
            buildings = paginator.page(1)
        except EmptyPage:
            buildings = paginator.page(paginator.num_pages)

        return render(request, "administrator/buildings/list.html", {"buildings": buildings})

    @staticmethod
    def building_delete_view(request, building_id):
        template = loader.get_template("administrator/buildings/list.html")
        if not BuildingService.delete(building_id):
            return HttpResponse(template.render({"errors": ["Failed to delete building"]}, request))
        return redirect("/buildings/")

    @staticmethod
    def building_create_view(request):
        form = BuildingForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/buildings/")
        template = loader.get_template("administrator/buildings/create.html")
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
        template = loader.get_template("administrator/buildings/update.html")
        return HttpResponse(template.render({"form": form}, request))
