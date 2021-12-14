from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from reservations import views

router = routers.DefaultRouter()
router.register(r"^persons", views.AdminPersonViewSet)
router.register(r"^buildings", views.AdminBuildingViewSet)
router.register(r"^groups", views.AdminGroupViewSet)
router.register(r"^reservation_statuses", views.AdminReservationStatusViewSet)
router.register(r"^reservations", views.AdminReservationViewSet)
router.register(r"^rooms", views.AdminRoomViewSet)

urlpatterns = [
    path(r"api/", include(router.urls)),
    path("", views.RoomTemplateView.public_rooms_get_view, name="index"),
    path("public-rooms/", views.RoomTemplateView.public_rooms_get_view, name="public_room_list"),
    path("public-rooms/<int:room_id>/", views.RoomTemplateView.public_room_get_view, name="public_room_view"),
    path("reservations/create", views.ReservationTemplateView.reservation_create_view, name="reservation_create"),
    path("login", auth_views.LoginView.as_view(redirect_field_name="/"), name="login"),
    path("logout", auth_views.LogoutView.as_view(redirect_field_name="/"), name="logout"),
]
