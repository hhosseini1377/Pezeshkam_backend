from django.shortcuts import render
from rest_framework.response import Response
from .models import Reservation
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from .serializers import patient_profile_serializer, patient_reservation_serializer, doctor_profile_serializer, doctor_reservation_serializer
# Create your views here.


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def patient_profile(request):
    patient_id = request.query_params['patient_id']
    patient = CustomUser.objects.get(pk=patient_id)
    patient_serializer = patient_profile_serializer(patient)
    return Response(patient_serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def patient_reservations(request):
    patient_id = request.query_params['patient_id']
    patient = CustomUser.objects.get(pk=patient_id)
    reservations = Reservation.objects.get(patient=patient)
    reservations_serializer = patient_reservation_serializer(reservations)
    return Response(reservations_serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctor_profile(request):
    doctor_id = request.query_params['doctor_id']
    doctor = CustomUser.objects.get(pk=doctor_id)
    doctor_serializer = doctor_profile_serializer(doctor)
    return Response(doctor_serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctor_reservations(request):
    doctor_id = request.query_params['doctor_id']
    doctor = CustomUser.objects.get(pk=doctor_id)
    reservations = Reservation.objects.get(doctor=doctor)
    reservations_serializer = doctor_reservation_serializer(reservations)
    return Response(reservations_serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctors(request):
    all_doctors = CustomUser.objects.filter(is_doctor=True)
    serializer = UserSerializer(all_doctors, many=True)
    return Response(serializer.data)
