from django.urls import include, path

from . import views

urlpatterns = [
    path('patient_profile/', views.patient_profile),
    path('patient_reservations/', views.patient_reservations),
    path('doctor_profile/', views.doctor_profile),
    path('doctor_reservations/', views.doctor_reservations),
    path('all_doctors/', views.doctors),
    path('delete_reservation/', views.delete_reservation),
    path('delete_patient_reservation/', views.delete_patient_reservation)
]