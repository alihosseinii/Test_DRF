from rest_framework import serializers
from .models import UserInformation, Reservation, IdentityInformation
from django.contrib.auth.hashers import make_password
from train.models import ExistTrains
import re

class SingupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = ["phone_number", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "phone_number": {"required": True}
        }
    

    def validate_phone_number(self, value):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("شماره تلفن باید با 09 شروع شود و دقیقاً 11 رقم عددی باشد.")
        return value
    
    def validate(self, data):
        data['username'] = data['phone_number']
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = super().create(validated_data)
        IdentityInformation.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        try:
            user = UserInformation.objects.get(phone_number=data.get("phone_number"))
        except UserInformation.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.check_password(data.get("password")):
            raise serializers.ValidationError("Invalid credentials")
        
        data["user"] = user
        return data


class TrainSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExistTrains
        fields = ['id', 'traintype', 'origin', 'destination', 'depratordate', 'depratortime', 'price']

class ReservationSerializer(serializers.ModelSerializer):
    train = TrainSimpleSerializer(read_only=True)  # فقط برای نمایش
    
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'train', 'quantity', 'total_price', 'reserved_at']
        read_only_fields = ['user', 'total_price', 'reserved_at']

    def create(self, validated_data):
        user = self.context["request"].user
        return Reservation.objects.create(user=user, **validated_data)
    

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityInformation
        exclude = ['user']