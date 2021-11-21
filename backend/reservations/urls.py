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

    path('buildings/<int:building_id>/', reservations.views.BuildingTemplateView.building_get_view, name='building_view'),
    path('buildings/', reservations.views.BuildingTemplateView.buildings_get_view, name='building_list'),
    path('buildings/<int:building_id>/delete', reservations.views.BuildingTemplateView.building_delete_view, name='building_delete'),
    path('buildings/create', reservations.views.BuildingTemplateView.building_create_view, name='person_create'),
    path('buildings/<int:building_id>/edit', reservations.views.BuildingTemplateView.building_edit_view, name='building_update'),

    path('rooms/<int:room_id>/', reservations.views.RoomTemplateView.room_get_view, name='room_view'),
    path('rooms/', reservations.views.RoomTemplateView.rooms_get_view, name='room_list'),
    path('rooms/<int:room_id>/delete', reservations.views.RoomTemplateView.room_delete_view, name='room_delete'),
    path('rooms/create', reservations.views.RoomTemplateView.room_create_view, name='person_create'),
    path('rooms/<int:room_id>/edit', reservations.views.RoomTemplateView.room_edit_view, name='room_update'),

    path('groups/<int:group_id>/', reservations.views.GroupTemplateView.group_get_view, name='group_view'),
    path('groups/', reservations.views.GroupTemplateView.groups_get_view, name='group_list'),
    path('groups/<int:group_id>/delete', reservations.views.GroupTemplateView.group_delete_view, name='group_delete'),
    path('groups/create', reservations.views.GroupTemplateView.group_create_view, name='person_create'),
    path('groups/<int:group_id>/edit', reservations.views.GroupTemplateView.group_edit_view, name='group_update'),

    path('reservationstatuses/<int:reservation_status_id>/', reservations.views.ReservationStatusTemplateView.reservation_status_get_view, name='reservation_status_view'),
    path('reservationstatuses/', reservations.views.ReservationStatusTemplateView.reservation_statuses_get_view, name='reservation_status_list'),
    path('reservationstatuses/<int:reservation_status_id>/delete', reservations.views.ReservationStatusTemplateView.reservation_status_delete_view, name='reservation_status_delete'),
    path('reservationstatuses/create', reservations.views.ReservationStatusTemplateView.reservation_status_create_view, name='reservation_status_create'),
    path('reservationstatuses/<int:reservation_status_id>/edit', reservations.views.ReservationStatusTemplateView.reservation_status_edit_view, name='reservation_status_update'),

    path('reservations/<int:reservation_id>/', reservations.views.ReservationTemplateView.reservation_get_view, name='reservation_view'),
    path('reservations/', reservations.views.ReservationTemplateView.reservations_get_view, name='reservation_list'),
    path('reservations/<int:reservation_id>/delete', reservations.views.ReservationTemplateView.reservation_delete_view, name='reservation_delete'),
    path('reservations/create', reservations.views.ReservationTemplateView.reservation_create_view, name='person_create'),
    path('reservations/<int:reservation_id>/edit', reservations.views.ReservationTemplateView.reservation_edit_view, name='reservation_update'),
]
