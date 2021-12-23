from enum import Enum
from django.db import models

from django.contrib.auth.models import User


class Person(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=20, blank=True)
    occupy = models.ManyToManyField(
        "Room",
        related_name="occupies",
        blank=True,
    )

    class Meta:
        permissions = (
            ("is_group_manager", "Can manage group"),
            ("is_room_manager", "Can manage room"),
        )

    def __str__(self):
        return "%s, %s%s" % (self.name, self.surname, " (admin)" if self.is_admin else "")

    @property
    def name(self):
        return self.user.first_name

    @name.setter
    def name(self, val):
        self.user.first_name = val
        self.user.save()

    @property
    def surname(self):
        return self.user.last_name

    @surname.setter
    def surname(self, val):
        self.user.last_name = val
        self.user.save()

    @property
    def is_admin(self):
        return self.user.is_superuser

    @is_admin.setter
    def is_admin(self, val):
        self.user.is_superuser = val
        self.user.save()

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, val):
        self.user.email = val
        self.user.save()


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % (self.name)


class Group(models.Model):
    name = models.CharField(max_length=50)

    parent = models.ForeignKey("Group", null=True, blank=True, on_delete=models.CASCADE)

    member = models.ManyToManyField(
        "Person",
        related_name="member",
        blank=True,
    )

    manager = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (manager: %s)" % (self.name, self.manager)


class Room(models.Model):
    name = models.CharField(max_length=50)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

    manager = models.ForeignKey(Person, on_delete=models.CASCADE)

    locked = models.BooleanField(default=True)

    def __str__(self):
        return "%s (building: %s)" % (self.name, self.building)


class ReservationStatus(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    dt_modified = models.DateTimeField(auto_now=True)

    APPROVED = "Approved"
    DECLINED = "Declined"
    PENDING_AUTHORISATION = "Pending authorisation"
    EXPIRED = "Expired"

    CHOICES = (
        (APPROVED, APPROVED),
        (DECLINED, DECLINED),
        (PENDING_AUTHORISATION, PENDING_AUTHORISATION),
        (EXPIRED, EXPIRED),
    )

    status = models.CharField(max_length=32, choices=CHOICES, default=PENDING_AUTHORISATION)
    note = models.TextField()

    def __str__(self):
        return "[%s], (by: %s, modified: %s)" % (self.status, self.author.__str__(), self.dt_modified)


class Reservation(models.Model):
    author = models.ForeignKey(Person, related_name="author", on_delete=models.CASCADE)
    owner = models.ForeignKey(Person, related_name="owner", null=True, blank=True, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(Person, related_name="attendee", blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # the last modified one is what we want
    reservation_status = models.ManyToManyField(ReservationStatus, related_name="reservation_status", blank=True)
    dt_from = models.DateTimeField()
    dt_to = models.DateTimeField()
    dt_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[%s] %s, (from: %s to: s%s, by %s, attendees: %s" % (
            self.reservation_status.last().status if hasattr(self.reservation_status.last(), "status") else "None",
            self.room,
            self.dt_from,
            self.dt_to,
            self.author,
            str([str(a) for a in self.attendees.all()]),
        )

    def current_status(self):
        return self.reservation_status.last() if hasattr(self.reservation_status.last(), "status") else False
