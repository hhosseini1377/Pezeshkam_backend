from django.urls import include, path

from . import views

urlpatterns = [
    path('user_profile/', views.user_profile),
    path('all_doctors/', views.doctors),
    path('delete_reservation/', views.delete_reservation),
    path('delete_patient_reservation/', views.delete_patient_reservation),
    path('set_profile/', views.set_profile),
    path('edit_profile/', views.edit_profile),
    path('get_id/', views.get_user_id),
    path('search_doctor/', views.search_doctor),
    path('reserve/', views.reserve),
    path('create_reservation/', views.create_reservation)
]