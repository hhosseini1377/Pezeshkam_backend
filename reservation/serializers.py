from rest_framework import serializers
from .models import Reservation
from users.models import CustomUser
from users.serializers import UserSerializer


class patient_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'username', 'password', 'pk', 'avatar')


class patient_reservation_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        depth = 1


class doctor_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('name', 'phone_number', 'username', 'password', 'field', 'pk', 'avatar')


class doctor_reservation_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        depth = 1

class get_user_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk')