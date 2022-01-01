from django.contrib.auth import views as auth_views
from reservations import views
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

router = routers.DefaultRouter()

router.register(r"^persons", views.AdminPersonViewSet)
router.register(r"^buildings", views.AdminBuildingViewSet)
router.register(r"^groups", views.AdminGroupViewSet)
router.register(r"^reservation_statuses", views.AdminReservationStatusViewSet)
router.register(r"^reservations", views.AdminReservationViewSet)
router.register(r"^rooms", views.AdminRoomViewSet)

urlpatterns = [
    path("", views.RoomTemplateView.public_rooms_get_view, name="index"),
    path("admin/", admin.site.urls),
    path(r"administrator/", include("reservations.administratorurls")),
    path(r"api/", include(router.urls)),
    path("public-rooms/", views.RoomTemplateView.public_rooms_get_view, name="public_room_list"),
    path("public-rooms/<int:room_id>/", views.RoomTemplateView.public_room_get_view, name="public_room_view"),
    path("reservations/create", views.ReservationTemplateView.reservation_create_view, name="reservation_create"),
    path("my-reservations", views.ReservationTemplateView.reservations_get_view, name="my_reservations_list"),
    path("login", views.CustomLoginView.as_view(redirect_field_name="/"), name="login"),
    path("logout", auth_views.LogoutView.as_view(redirect_field_name="/"), name="logout"),
]
