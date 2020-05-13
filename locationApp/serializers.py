from userApp.models import *
from rest_framework import serializers


class LocationWasteInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWasteInformation
        fields = ("dong", "discharge_day", 'house_start', 'house_end', 'food_start', 'food_end'
                  , 'house_method', 'food_method', 'recycle_method', 'house_day', 'food_day', 'recycle_day')


