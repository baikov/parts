from django.db.models import fields
from rest_framework import serializers

from .models import Part

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ['id', 'vin', 'code', 'name', 'count', 'unit', 'image']