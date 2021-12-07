from django.urls import include, path

from reservations import views

urlpatterns = [
    path("persons/<int:person_id>/", views.AdminPersonTemplateView.person_get_view, name="admin_person_view"),
    path("persons/", views.AdminPersonTemplateView.persons_get_view, name="admin_person_list"),
    path(
        "persons/<int:person_id>/delete", views.AdminPersonTemplateView.person_delete_view, name="admin_person_delete"
    ),
    path("persons/create", views.AdminPersonTemplateView.person_create_view, name="admin_person_create"),
    path("persons/<int:person_id>/edit", views.AdminPersonTemplateView.person_edit_view, name="admin_person_update"),
    path("buildings/<int:building_id>/", views.AdminBuildingTemplateView.building_get_view, name="admin_building_view"),
    path("buildings/", views.AdminBuildingTemplateView.buildings_get_view, name="admin_building_list"),
    path(
        "buildings/<int:building_id>/delete",
        views.AdminBuildingTemplateView.building_delete_view,
        name="admin_building_delete",
    ),
    path("buildings/create", views.AdminBuildingTemplateView.building_create_view, name="admin_building_create"),
    path(
        "buildings/<int:building_id>/edit",
        views.AdminBuildingTemplateView.building_edit_view,
        name="admin_building_update",
    ),
    path("rooms/<int:room_id>/", views.AdminRoomTemplateView.room_get_view, name="admin_room_view"),
    path("rooms/", views.AdminRoomTemplateView.rooms_get_view, name="admin_room_list"),
    path("rooms/<int:room_id>/delete", views.AdminRoomTemplateView.room_delete_view, name="admin_room_delete"),
    path("rooms/create", views.AdminRoomTemplateView.room_create_view, name="admin_room_create"),
    path("rooms/<int:room_id>/edit", views.AdminRoomTemplateView.room_edit_view, name="admin_room_update"),
    path("groups/<int:group_id>/", views.AdminGroupTemplateView.group_get_view, name="admin_group_view"),
    path("groups/", views.AdminGroupTemplateView.groups_get_view, name="admin_group_list"),
    path("groups/<int:group_id>/delete", views.AdminGroupTemplateView.group_delete_view, name="admin_group_delete"),
    path("groups/create", views.AdminGroupTemplateView.group_create_view, name="admin_group_create"),
    path("groups/<int:group_id>/edit", views.AdminGroupTemplateView.group_edit_view, name="admin_group_update"),
    path(
        "reservationstatuses/<int:reservation_status_id>/",
        views.AdminReservationStatusTemplateView.reservation_status_get_view,
        name="admin_reservation_status_view",
    ),
    path(
        "reservationstatuses/",
        views.AdminReservationStatusTemplateView.reservation_statuses_get_view,
        name="admin_reservation_status_list",
    ),
    path(
        "reservationstatuses/<int:reservation_status_id>/delete",
        views.AdminReservationStatusTemplateView.reservation_status_delete_view,
        name="admin_reservation_status_delete",
    ),
    path(
        "reservationstatuses/create",
        views.AdminReservationStatusTemplateView.reservation_status_create_view,
        name="admin_reservation_status_create",
    ),
    path(
        "reservationstatuses/<int:reservation_status_id>/edit",
        views.AdminReservationStatusTemplateView.reservation_status_edit_view,
        name="admin_reservation_status_update",
    ),
    path(
        "reservations/<int:reservation_id>/",
        views.AdminReservationTemplateView.reservation_get_view,
        name="admin_reservation_view",
    ),
    path("reservations/", views.AdminReservationTemplateView.reservations_get_view, name="admin_reservation_list"),
    path(
        "reservations/<int:reservation_id>/delete",
        views.AdminReservationTemplateView.reservation_delete_view,
        name="admin_reservation_delete",
    ),
    path(
        "reservations/create",
        views.AdminReservationTemplateView.reservation_create_view,
        name="admin_reservation_create",
    ),
    path(
        "reservations/<int:reservation_id>/edit",
        views.AdminReservationTemplateView.reservation_edit_view,
        name="admin_reservation_update",
    ),
    path(
        "reservations/<int:reservation_id>/statuses/create",
        views.AdminReservationStatusTemplateView.status_create_view,
        name="admin_status_create"
    )
]
