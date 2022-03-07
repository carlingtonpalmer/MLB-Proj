from rest_framework import serializers
from . import models


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields = ('user', 'title', 'details')
        read_only_fields = ['user']