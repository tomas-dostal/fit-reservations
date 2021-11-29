from django.urls import include, path

from reservations import views

urlpatterns = [
    path("persons/<int:person_id>/", views.PersonTemplateView.person_get_view, name="admin_person_view"),
    path("persons/", views.PersonTemplateView.persons_get_view, name="admin_person_list"),
    path("persons/<int:person_id>/delete", views.PersonTemplateView.person_delete_view,
         name="admin_person_delete"),
    path("persons/create", views.PersonTemplateView.person_create_view, name="admin_person_create"),
    path("persons/<int:person_id>/edit", views.PersonTemplateView.person_edit_view, name="admin_person_update"),
    path("buildings/<int:building_id>/", views.BuildingTemplateView.building_get_view,
         name="admin_building_view"),
    path("buildings/", views.BuildingTemplateView.buildings_get_view, name="admin_building_list"),
    path(
        "buildings/<int:building_id>/delete",
        views.BuildingTemplateView.building_delete_view,
        name="admin_building_delete",
    ),
    path("buildings/create", views.BuildingTemplateView.building_create_view, name="admin_building_create"),
    path(
        "buildings/<int:building_id>/edit",
        views.BuildingTemplateView.building_edit_view,
        name="admin_building_update",
    ),
    path("rooms/<int:room_id>/", views.RoomTemplateView.room_get_view, name="admin_room_view"),
    path("rooms/", views.RoomTemplateView.rooms_get_view, name="admin_room_list"),
    path("rooms/<int:room_id>/delete", views.RoomTemplateView.room_delete_view, name="admin_room_delete"),
    path("rooms/create", views.RoomTemplateView.room_create_view, name="admin_room_create"),
    path("rooms/<int:room_id>/edit", views.RoomTemplateView.room_edit_view, name="admin_room_update"),
    path("groups/<int:group_id>/", views.GroupTemplateView.group_get_view, name="admin_group_view"),
    path("groups/", views.GroupTemplateView.groups_get_view, name="admin_group_list"),
    path("groups/<int:group_id>/delete", views.GroupTemplateView.group_delete_view, name="admin_group_delete"),
    path("groups/create", views.GroupTemplateView.group_create_view, name="admin_group_create"),
    path("groups/<int:group_id>/edit", views.GroupTemplateView.group_edit_view, name="admin_group_update"),
    path(
        "reservationstatuses/<int:reservation_status_id>/",
        views.ReservationStatusTemplateView.reservation_status_get_view,
        name="admin_reservation_status_view",
    ),
    path(
        "reservationstatuses/",
        views.ReservationStatusTemplateView.reservation_statuses_get_view,
        name="admin_reservation_status_list",
    ),
    path(
        "reservationstatuses/<int:reservation_status_id>/delete",
        views.ReservationStatusTemplateView.reservation_status_delete_view,
        name="admin_reservation_status_delete",
    ),
    path(
        "reservationstatuses/create",
        views.ReservationStatusTemplateView.reservation_status_create_view,
        name="admin_reservation_status_create",
    ),
    path(
        "reservationstatuses/<int:reservation_status_id>/edit",
        views.ReservationStatusTemplateView.reservation_status_edit_view,
        name="admin_reservation_status_update",
    ),
    path(
        "reservations/<int:reservation_id>/",
        views.ReservationTemplateView.reservation_get_view,
        name="admin_reservation_view",
    ),
    path("reservations/", views.ReservationTemplateView.reservations_get_view, name="admin_reservation_list"),
    path(
        "reservations/<int:reservation_id>/delete",
        views.ReservationTemplateView.reservation_delete_view,
        name="admin_reservation_delete",
    ),
    path("reservations/create", views.ReservationTemplateView.reservation_create_view,
         name="admin_reservation_create"),
    path(
        "reservations/<int:reservation_id>/edit",
        views.ReservationTemplateView.reservation_edit_view,
        name="admin_reservation_update",
    )
]
