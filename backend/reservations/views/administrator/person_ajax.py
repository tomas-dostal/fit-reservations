from ajax_datatable.views import AjaxDatatableView
from django.template.loader import render_to_string
from django.urls import reverse
from reservations.models import Person


class AdminPersonAjaxTemplateView(AjaxDatatableView):
    model = Person
    title = 'Persons'
    initial_order = [["id", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'id', "title": "Id", 'foreign_field': 'user__id', 'visible': True},
        {'name': 'firstname', "title": "Jméno", 'foreign_field': 'user__first_name', 'visible': True},
        {'name': 'lastname', "title": "Příjmení", 'foreign_field': 'user__last_name', 'visible': True},
        {'name': 'is_admin', 'title': 'Administrátor', 'visible': True, 'boolean': True, "searchable": False, "orderable": False},

        {'name': 'edit', 'title': 'Upravit', 'visible': True, "searchable": False, "orderable": False,
         'autofilter': False},
        {'name': 'delete', 'title': 'Smazat', 'visible': True, "searchable": False, "orderable": False,
         'autofilter': False},
    ]

    def customize_row(self, row, obj):
        # 'row' is a dictionary representing the current row, and 'obj' is the current object.
        detail = reverse("admin_person_view", kwargs={"person_id": obj.id})
        row["pk"] = "<a href='" + detail + "' class='id'>" + str(row["pk"]) + "</a>"

        edit = reverse("admin_person_update", kwargs={"person_id": obj.id})
        row["edit"] = "<a href='" + edit + "' class='button green'>Upravit</a>"

        delete = reverse("admin_person_delete", kwargs={"person_id": obj.id})
        row["delete"] = "<a href='" + delete + "' class='button red'>Smazat</a>"

        return row
