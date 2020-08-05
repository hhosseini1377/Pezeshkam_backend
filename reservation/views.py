from json import loads

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.utils import json

from .models import Reservation
from users.models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserSerializer
from .serializers import patient_profile_serializer, patient_reservation_serializer, doctor_profile_serializer, \
    doctor_reservation_serializer, get_user_serializer, user_avatar_serializer


# Create your views here.


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def user_profile(request):
    user_id = request.query_params['user_id']
    user = CustomUser.objects.get(pk=user_id)
    if not user.is_doctor:
        patient_serializer = patient_profile_serializer(user)
        reservations = Reservation.objects.filter(patient=user)
        reservations_serializer = patient_reservation_serializer(reservations, many=True)
        return Response([patient_serializer.data, reservations_serializer.data])
    else:
        doctor_serializer = doctor_profile_serializer(user)
        reservations = Reservation.objects.filter(doctor=user)
        reservations_serializer = doctor_reservation_serializer(reservations, many=True)
        return Response([doctor_serializer.data, reservations_serializer.data])


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def doctors(request):
    all_doctors = CustomUser.objects.filter(is_doctor=True)
    serializer = UserSerializer(all_doctors, many=True)
    user = request.user
    avatar_serializer = user_avatar_serializer(user)
    return Response([serializer.data, avatar_serializer.data])


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
    if request.data['is_doctor']:
        user.avatar = 'default_doctor.jpg'
    else:
        user.avatar = 'default_patient.jpg'
    user.save()
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
    user = request.user
    serializer = get_user_serializer(user)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def search_doctor(request):
    search_text = request.query_params['search']
    searched_doctors = (
                CustomUser.objects.filter(is_doctor=True, username__contains=search_text) | CustomUser.objects.filter(
            is_doctor=True, field__contains=search_text)).distinct()
    search_serializer = doctor_profile_serializer(searched_doctors, many=True)
    return Response(search_serializer.data)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def reserve(request):
    patient_id = request.data['patient_id']
    reservation_id = request.data['reservation_id']
    patient = CustomUser.objects.get(pk=patient_id)
    reservation = Reservation.objects.get(pk=reservation_id)
    reservation.patient = patient
    reservation.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
def create_reservation(request):
    doctor_id = request.data['doctor_id']
    doctor = CustomUser.objects.get(pk=doctor_id)
    day = int(request.data['day'])
    month = int(request.data['month'])
    year = int(request.data['year'])
    start_hour = int(request.data['start_hour'])
    end_hour = int(request.data['end_hour'])
    start_minute = int(request.data['start_minute'])
    end_minute = int(request.data['end_minute'])
    period = int(request.data['period'])
    is_valid = True
    if day > 31 or day < 1:
        is_valid = False
    elif month < 1 or month > 12:
        is_valid = False
    elif year < 1399:
        is_valid = False
    if not is_valid:
        res = {'message': 'تاریخ وارد شده معتبر نمی‌باشد.'}
        return Response(res, status=status.HTTP_200_OK)
    reservations = list(Reservation.objects.filter(doctor=doctor, day=day, month=month, year=year))
    start_time = 60 * start_hour + start_minute
    end_time = 60 * end_hour + end_minute
    for reservation in reservations:
        reservation_start_time = 60 * int(reservation.start_hour) + int(reservation.start_minute)
        reservation_end_time = 60 * int(reservation.end_hour) + int(reservation.end_minute)
        if start_time < reservation_start_time < end_time:
            is_valid = False
        elif start_time < reservation_end_time < end_time:
            is_valid = False
    if not is_valid:
        res = {'message': 'تداخل زمانی میان زمان‌‌های رزرو این روز و زمان‌های وارد شده توسط شما وجود دارد.'}
        return Response(res, status=status.HTTP_200_OK)
    if start_hour > 24 or end_hour > 24:
        is_valid = False
    if start_minute > 60 or end_minute > 60:
        is_valid = False
    if end_time < start_time:
        is_valid = False
    if (end_time - start_time) % period != 0:
        res = {'message': 'زمان‌های وارد شده با بازه زمانی مطابقت ندارد.'}
        return Response(res, status=status.HTTP_200_OK)
    if not is_valid:
        res = {'message': 'زمان‌های وارد شده معتبر نمی‌باشند.'}
        return Response(res, status=status.HTTP_200_OK)

    times_num = int((end_time - start_time) / period)
    end_time = start_time
    end_time += period
    for i in range(0, times_num):
        start_hour = int(start_time / 60)
        start_minute = start_time % 60
        end_hour = int(end_time / 60)
        end_minute = end_time % 60
        Reservation.objects.create(doctor=doctor, start_hour=str(start_hour), end_hour=str(end_hour), start_minute=str(start_minute),
                                   end_minute=str(end_minute), year=str(year), month=str(month), day=str(day))
        start_time += period
        end_time += period
    res = {'message': 'زمان‌های رزرو با موفقیت اضافه شدند.'}
    return Response((json.dumps(res)), status=status.HTTP_200_OK)


