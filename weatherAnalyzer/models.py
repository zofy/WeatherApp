from __future__ import unicode_literals

from django.core.validators import MinLengthValidator
from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=15, validators=[
        MinLengthValidator(6, message='Password must consist of at least 6 characters.')])
    latitude = models.CharField(max_length=10, default='0')
    longitude = models.CharField(max_length=10, default='0')
    city = models.CharField(max_length=20, default=None)
    country = models.CharField(max_length=20, default=None)
    location = (latitude, longitude, city)

    def __str__(self):
        return 'Email: ' + self.email + ' location: ' + self.location[0] + ', ' + self.location[1] + self.location[
            2] + ' Country: ' + self.location[3]
