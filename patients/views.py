from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer, PatientUpdateSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def patient_list_create(request):
    """
    GET: Retrieve all patients for the authenticated user
    POST: Create a new patient
    """
    if request.method == 'GET':
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PatientCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            patient = serializer.save(created_by=request.user)
            return Response({
                'message': 'Patient created successfully',
                'data': PatientSerializer(patient).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def patient_detail(request, pk):
    """
    GET: Retrieve a specific patient
    PUT: Update a patient
    DELETE: Delete a patient
    """
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)
    
    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = PatientUpdateSerializer(
            patient, 
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            patient = serializer.save()
            return Response({
                'message': 'Patient updated successfully',
                'data': PatientSerializer(patient).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        patient.delete()
        return Response({
            'message': 'Patient deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
