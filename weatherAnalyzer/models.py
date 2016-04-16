from __future__ import unicode_literals

from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(models.Manager):
    def create_user(self, email, password, location):
        user = User(email=email, password=password)
        Location.objects.create_location(user=user, location=location)
        user.save()
        return user


class User(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=15, validators=[
        MinLengthValidator(6, message='Password must consist of at least 6 characters.')])

    objects = UserManager()

    def __str__(self):
        return 'Email: ' + self.email + ', ' + 'password: ' + self.password


class LocationManager(models.Manager):
    def create_location(self, user, location):
        l = Location(user=user, latitude=location.get('latitude'), longitude=location.get('longitude'),
                     city=location.get('city'))
        l.save()
        return l

    def change_location(self):
        pass


class Location(models.Model):
    user = models.OneToOneField(User)
    latitude = models.CharField(max_length=10, default='0')
    longitude = models.CharField(max_length=10, default='0')
    city = models.CharField(max_length=20, default=None)
    country = models.CharField(max_length=20, default=None)

    objects = LocationManager()

    def __str__(self):
        return 'Email: ' + self.user.email + ' location: ' + self.latitude + ', ' + self.longitude + ', ' + self.city + ', ' + self.country
