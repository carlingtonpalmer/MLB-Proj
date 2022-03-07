from django.db import models
from django.conf import settings

# Create your models here.

class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_type = models.CharField(verbose_name='request type', max_length=50)
    pickup = models.CharField(verbose_name='pickup', max_length=250)
    dropoff = models.CharField(verbose_name='dropoff', max_length=250)
    request_time = models.DateTimeField(auto_now_add=True, blank=True)

