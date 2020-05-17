from rest_framework import serializers
from .models import *


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class CategoryRegulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRegulation
        fields = ('cg_name', )


class WasteCategorySSerializer(serializers.ModelSerializer):

    regulation = CategoryRegulationSerializer(source= 'categoryregulation_set', many=True)

    class Meta:
        model = WasteCategoryM
        fields = ('idx', 'cg_name', 'regulation')

class PointHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PointHistory
        fields =('value',)