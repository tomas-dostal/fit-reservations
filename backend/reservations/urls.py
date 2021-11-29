from django.urls import include, path

from rest_framework import routers

from reservations import views

router = routers.DefaultRouter()
router.register(r"^persons", views.PersonViewSet)
router.register(r"^buildings", views.BuildingViewSet)
router.register(r"^groups", views.GroupViewSet)
router.register(r"^reservation_statuses", views.ReservationStatusViewSet)
router.register(r"^reservations", views.ReservationViewSet)
router.register(r"^rooms", views.RoomViewSet)

urlpatterns = [
    path(r"api/", include(router.urls))
]
