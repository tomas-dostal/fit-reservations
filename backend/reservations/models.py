from enum import Enum

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return "%s, %s" % (self.surname, self.name)


class Building(models.Model):
    name = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=50)
    subgroup = models.ManyToManyField("self")

    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name


class Room(models.Model):
    name = models.CharField(max_length=50)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s (building: %s)" % (self.name, self.building)

class ReservationStatus(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    APPROVED = 'Approved'
    DECLINED = 'Declined'
    PENDING_AUTHORISATION = 'Pending authorisation'
    EXPIRED = 'Expired'

    CHOICES = (
        (APPROVED, APPROVED),
        (DECLINED, DECLINED),
        (PENDING_AUTHORISATION, PENDING_AUTHORISATION),
        (EXPIRED, EXPIRED)
    )

    status = models.CharField(max_length=32, choices=CHOICES, default=PENDING_AUTHORISATION)
    note = models.TextField()

class Reservation(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="attendee")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation_status = models.ForeignKey(ReservationStatus, on_delete=models.CASCADE)
    dt_from = models.DateTimeField()
    dt_to = models.DateTimeField()
    dt_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "author: %s (%s, from: %s to: %s)" % (self.author, self.room, self.dt_from, self.dt_to)
