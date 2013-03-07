from django.db import models

class subscriber(models.Model):
    email = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add = True)
    subscribed = models.BooleanField(default=True)