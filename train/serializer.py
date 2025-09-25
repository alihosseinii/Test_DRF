from rest_framework import serializers
from .models import ExistTrains, City


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistTrains
        fields = [ 'id', 'traintype', 'depratordate', 'price', 'returndate', 'returntime', 'origin', 'destination', 'available']

class TrainDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistTrains
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
