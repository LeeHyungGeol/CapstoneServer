from rest_framework import serializers
from .models import *
from DetectionApp.serializers import CategoryRegulationSerializer

class MeasureUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ('image',)

class MeasureHistorySerializer(serializers.ModelSerializer):

    msg = serializers.CharField(max_length=45, required=False)
    code = serializers.IntegerField( required=False)


    class Meta:
        model = MeasureHistory
        fields = ['idx', 'user_idx', 'image', 'width', 'height', 'msg', 'code']

class MatchFeeSerializer(serializers.Serializer):
    cg_name = serializers.CharField(max_length=100)
    width = serializers.FloatField()
    height = serializers.FloatField()
