from django.urls import include, path

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
    path(r"api/", include(router.urls))
]
