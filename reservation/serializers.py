from rest_framework import serializers
from .models import Reservation
from users.models import CustomUser


class patient_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'username', 'password')


class reservation_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
