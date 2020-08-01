from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Doctor
from .serlializers import DoctorSerializer
# Create your views here.


@api_view(['GET', ])
def get_profile(request):
    doctor_id = request.query_params.get('doctor_id', None)
    doctor = Doctor.objects.get(pk=doctor_id)
    doctor_serializer = DoctorSerializer(doctor)
    return Response(doctor_serializer.data)