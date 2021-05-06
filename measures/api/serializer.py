from rest_framework import serializers
from ..models import Measure

class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = '__all__'


class MeasureGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields = ['value', 'creation_date']
