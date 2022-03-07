from django.db import models
from django.conf import settings
# Create your models here.


class ContactUs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(verbose_name='title', max_length=255, null=False, blank=False)
    details = models.TextField(null=False, blank=False)
    # contact_time = models.DateTimeField(auto_now_add=True, blank=True)