from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
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
    reservations = Reservation.objects.filter(patient=patient)
    reservations_serializer = patient_reservation_serializer(reservations, many=True)
    return Response([patient_serializer.data, reservations_serializer.data])


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctor_profile(request):
    doctor_id = request.query_params['doctor_id']
    doctor = CustomUser.objects.get(pk=doctor_id)
    doctor_serializer = doctor_profile_serializer(doctor)
    reservations = Reservation.objects.filter(doctor=doctor)
    reservations_serializer = doctor_reservation_serializer(reservations, many=True)
    return Response([doctor_serializer.data, reservations_serializer.data])


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctors(request):
    all_doctors = CustomUser.objects.filter(is_doctor=True)
    serializer = UserSerializer(all_doctors, many=True)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def delete_reservation(request):
    reservation = Reservation.objects.get(pk=request.data['reservation_id'])
    reservation.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def delete_patient_reservation(request):
    reservation = Reservation.objects.get(pk=request.data['reservation_id'])
    reservation.patient = None
    reservation.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def set_profile(request):
    username = request.data['username']
    user = CustomUser.objects.get(username=username)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def edit_profile(request):
    user = CustomUser.objects.get(pk=request.data['user_id'])
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def get_user_id(request):
    return Response(request.user.pk)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def search_doctor(request):
    search_text = request.query_params['search']
    searched_doctors = (CustomUser.objects.filter(is_doctor=True, username__contains=search_text) | CustomUser.objects.filter(is_doctor=True, field__contains=search_text)).distinct()
    search_serializer = doctor_profile_serializer(searched_doctors, many=True)
    return Response(search_serializer.data)