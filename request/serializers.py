from rest_framework import serializers
from . import models


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Request
        fields = ('user', 'request_type', 'pickup', 'dropoff', 'request_time')
        read_only_fields = ['user', 'request_time']