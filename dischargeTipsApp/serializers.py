from rest_framework import serializers
from dischargeTipsApp.models import *


class DischargeTipsSerializer(serializers.ModelSerializer):
    category_m_name = serializers.CharField(source='category_m_idx.cg_name')
    class Meta:
        model = DischargeTips
        fields = ("idx", "category_m_name", 'content', 'item_corresponding', 'item_discorresponding')


class WasteCategoryLSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategoryL
        fields = ("idx", "cg_name")


class WasteCategoryMSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategoryM
        fields = ("idx", "cg_name", "cg_large_idx")


class WasteCategorySSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategoryS
        fields = ("idx", "cg_name", "cg_middle_idx", "label_name")