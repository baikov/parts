from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import NotFound

from .models import Part
from .serializers import PartSerializer

class PartViewset(generics.ListAPIView):
    serializer_class = PartSerializer

    def get_queryset(self):
        parts = Part.objects.all()
        vin = self.request.query_params.get('vin', None)
        if vin is not None:
            parts = parts.filter(vin=vin)
        return parts
