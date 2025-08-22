from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Doctor
from .serializers import DoctorSerializer, DoctorCreateSerializer, DoctorUpdateSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def doctor_list_create(request):
    """
    GET: Retrieve all doctors
    POST: Create a new doctor
    """
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response({
            'count': doctors.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = DoctorCreateSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor created successfully',
                'data': DoctorSerializer(doctor).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def doctor_detail(request, pk):
    """
    GET: Retrieve a specific doctor
    PUT: Update a doctor
    DELETE: Delete a doctor
    """
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = DoctorUpdateSerializer(doctor, data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor updated successfully',
                'data': DoctorSerializer(doctor).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        doctor.delete()
        return Response({
            'message': 'Doctor deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
