from reservations.models import *
from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class PersonService:
    @staticmethod
    def find_by_id(user_id):
        try:
            return Person.objects.get(pk=user_id)
        except Person.DoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Person.objects.all()

    @staticmethod
    def create(data):
        try:
            user = User.objects.create(
                username=data.get("email", "test2@email.com"),
                first_name=data.get("name"),
                last_name=data.get("surname"),
                email=data.get("email", "test2@email.com"),
                is_superuser=True if data.get("is_admin") else False,
            )
            # because this is setting the RAW password, in the constructor is used hash of the password
            user.set_password(data.get("password"))
            user.save()
            person = Person.objects.create(
                user=user,
                phone_number=data.get("phone_number"),
            )
            person.occupy.set(data.get("occupy"))
            person.save()

        except IntegrityError:
            return None

        return person

    @staticmethod
    def delete(user_id):
        try:
            person = Person.objects.get(pk=user_id)
            person.user.delete()
            Person.delete(person)
            return True
        except Person.DoesNotExist:
            return False
        except models.ProtectedError or models.RestrictedError:
            return False

    @staticmethod
    def update(person, data):
        try:
            user = person.user
            if data.get("password"):
                user.set_password(data.get("password"))
            person.user.username = data.get("email", "test2@email.com")
            person.user.first_name = data.get("name")
            person.user.last_name = data.get("surname")
            person.user.email = data.get("email", "test2@email.com")
            person.user.is_superuser = True if data.get("is_admin") else False
            person.user.save()

            person.phone_number = data.get("phone_number")
            person.occupy.set(data.get("occupy"))

            person.save()

            return True
        except Person.DoesNotExist:
            return False
