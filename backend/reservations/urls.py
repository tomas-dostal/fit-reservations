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
    path(r"", include(router.urls)),
]
