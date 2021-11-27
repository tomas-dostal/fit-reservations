from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from django.views.generic import ListView
from rest_framework import viewsets
from reservations.serializers import *
from reservations.models import *
from reservations.services import *
from reservations.forms import *
from backend.settings import DEFAULT_PAGE_SIZE


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonTemplateView(ListView):
    paginate_by = 10
    context_object_name = "person-list"

    @staticmethod
    def person_get_view(request, person_id):
        person = PersonService.find_by_id(person_id)
        template = loader.get_template("persons/detail.html")
        return HttpResponse(template.render({"person": person}, request))

    @staticmethod
    def persons_get_view(request):

        page = request.GET.get("page", 1)
        paginator = Paginator(PersonService.find_all(), DEFAULT_PAGE_SIZE)
        try:
            persons = paginator.page(page)
        except PageNotAnInteger:
            persons = paginator.page(1)
        except EmptyPage:
            persons = paginator.page(paginator.num_pages)

        return render(request, "persons/list.html", {"persons": persons})

    @staticmethod
    def person_delete_view(request, person_id):
        template = loader.get_template("persons/list.html")

        if not PersonService.delete(person_id):
            return HttpResponse(template.render({"errors": ["Failed to delete person"]}, request))
        return redirect("/persons/")

    @staticmethod
    def person_create_view(request):
        form = PersonForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("/persons/")

        template = loader.get_template("persons/create.html")
        return HttpResponse(template.render({"form": form}, request))

    @staticmethod
    def person_edit_view(request, person_id):
        instance = PersonService.find_by_id(person_id)
        if instance is None:
            raise Http404("Person does not exist")
        form = PersonForm(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/persons/")

        template = loader.get_template("persons/update.html")
        return HttpResponse(template.render({"form": form}, request))
