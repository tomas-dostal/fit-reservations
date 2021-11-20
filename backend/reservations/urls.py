from django.urls import include, path

from rest_framework import routers

from reservations.views import *

import reservations.views

router = routers.DefaultRouter()
router.register(r"^persons", reservations.views.PersonViewSet)
router.register(r"^buildings", reservations.views.BuildingViewSet)
router.register(r"^groups", reservations.views.GroupViewSet)
router.register(r"^reservation_statuses", reservations.views.ReservationStatusViewSet)
router.register(r"^reservations", reservations.views.ReservationViewSet)
router.register(r"^rooms", reservations.views.RoomViewSet)

urlpatterns = [
    path(r"api/", include(router.urls)),
    path('persons/<int:person_id>/', reservations.views.PersonTemplateView.person_get_view, name='person_view'),
    path('persons/', reservations.views.PersonTemplateView.persons_get_view, name='person_list'),
    path('persons/<int:person_id>/delete', reservations.views.PersonTemplateView.person_delete_view, name='person_delete'),
    path('persons/create', reservations.views.PersonTemplateView.person_create_view, name='person_create'),
    path('persons/<int:person_id>/edit', reservations.views.PersonTemplateView.person_edit_view, name='person_update'),
]
