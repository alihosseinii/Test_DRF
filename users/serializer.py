from rest_framework import serializers
from .models import UserInformation, Reservation, IdentityInformation, UserManager
from django.contrib.auth import authenticate

class singupserializer(serializers.ModelSerializer):
    class Meta:
        model = UserInformation
        fields = '__all__'

    def validate(self, attrs):
        phone = attrs.get('phone_number')
        if UserInformation.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("this phone is already rigestered")
        return super().validate(attrs)

    def create(self, validated_data):
        return UserInformation.objects.create_user(**validated_data)
    

class loginserializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)# i think this isnt work 

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")

        if not phone or not password:
            raise serializers.ValidationError("phone number and password are necessary")
        user = authenticate(username= phone, password=password)
        if user is None :
            raise serializers.ValidationError("information is incorrect")
        
        data["user"] = user
        return data
        
    
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        user = self.context["request"].user
        return Reservation.objects.create(user=user, **validated_data)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentityInformation
        fields = '__all__'