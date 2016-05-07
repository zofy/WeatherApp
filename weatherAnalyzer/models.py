from __future__ import unicode_literals

from django.core.validators import MinLengthValidator
from django.db import models


class UserManager(models.Manager):
    def create_user(self, email, password, location):
        user = User(email=email, password=password)
        user.save()
        Location.objects.create_location(user=user, location=location)
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
        l = Location(user=user, latitude=location.get('lat'), longitude=location.get('lng'),
                     city=location.get('city'))
        l.save()
        return l

    def change_location(self, user, loc):
        db_location = Location.objects.get(user=user)
        for data in loc:
            if loc[data] != getattr(db_location, data):
                setattr(db_location, data, loc[data])
        db_location.save()
        return db_location


class Location(models.Model):
    user = models.OneToOneField(User)
    lat = models.CharField(max_length=10, default='0')
    lng = models.CharField(max_length=10, default='0')
    city = models.CharField(max_length=20, default=None)
    # country = models.CharField(max_length=20, default=None)

    def get_dict(self):
        return {'lat': self.lat, 'lng': self.lng, 'city': self.city}

    objects = LocationManager()

    def __str__(self):
        return 'Email: ' + self.user.email + ' location: ' + self.lat + ', ' + self.lng + ', ' + self.city
