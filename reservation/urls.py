from django.urls import include, path

from . import views



urlpatterns = [
    path('patient_profile/', views.patient_profile),
    path('doctor_profile/', views.doctor_profile),
    path('all_doctors/', views.doctors),
    path('delete_reservation/', views.delete_reservation),
    path('delete_patient_reservation/', views.delete_patient_reservation),
    path('set_profile/', views.set_profile),
    path('edit_profile/', views.edit_profile),
    path('get_id/', views.get_user_id),
    path('search_doctor/', views.search_doctor),

]