# Register your models here.
from django.contrib import admin

# the module name is app_name.models
from reservations.models import Person, Building, Group, Room, Reservation, ReservationStatus

admin.site.register(Person)
admin.site.register(Building)
admin.site.register(Group)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(ReservationStatus)
