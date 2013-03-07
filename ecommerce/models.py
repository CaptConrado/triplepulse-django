from django.db import models
from django.contrib.auth.models import User

class Shipment(models.Model):
    date = models.DateField()
    shipped = models.BooleanField(default=False)
    user = models.ForeignKey(User, unique=False)
    name = models.CharField(max_length=100)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zip = models.CharField(max_length=10)
    tracking_code = models.CharField(max_length=255, blank=True)
    STANDARD = '0'
    AID_STATION = '1'
    TYPE_CHOICES = (
        (STANDARD, 'Standard'),
        (AID_STATION, 'Aid Station'),

        )

    type = models.integerField(choices=TYPE_CHOICES)
    def __unicode__(self):
        return unicode(self.user) + ' | ' + unicode(self.date)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    stripe_id = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=20, blank=True)
    zip = models.CharField(max_length=10)
    def __unicode__(self):
        return unicode(self.user)


