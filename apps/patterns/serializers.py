from rest_framework import serializers
from .models import OcurrenceReport


class OcurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OcurrenceReport
        fields = ("id", "total", "ocurrences", "commit")
