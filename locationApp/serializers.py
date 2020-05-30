from userApp.models import LocationWasteInformation
from rest_framework import serializers


class LocationWasteInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationWasteInformation
        fields = '__all__'

