from rest_framework import serializers
from .models import *


class MeasureUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ('image',)