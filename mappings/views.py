from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import (
    PatientDoctorMappingSerializer, 
    PatientDoctorMappingCreateSerializer,
    PatientDoctorMappingDoctorOnlySerializer
)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mapping_list_create(request):
    """
    GET: Retrieve all patient-doctor mappings for the authenticated user
    POST: Create a new patient-doctor mapping
    """
    if request.method == 'GET':
        # Get mappings for patients created by the authenticated user
        from patients.models import Patient
        user_patients = Patient.objects.filter(created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(
            patient__in=user_patients,
            is_active=True
        )
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response({
            'count': mappings.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PatientDoctorMappingCreateSerializer(
            data=request.data, 
            context={'request': request}
        )
        if serializer.is_valid():
            mapping = serializer.save()
            return Response({
                'message': 'Patient-doctor mapping created successfully',
                'data': PatientDoctorMappingSerializer(mapping).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_doctors(request, patient_id):
    """
    GET: Retrieve all doctors assigned to a specific patient
    """
    # Ensure the patient belongs to the authenticated user
    from patients.models import Patient
    from patients.serializers import PatientSerializer
    
    patient = get_object_or_404(Patient, pk=patient_id, created_by=request.user)
    
    mappings = PatientDoctorMapping.objects.filter(
        patient=patient,
        is_active=True
    )
    
    # Use the doctor-only serializer to avoid repeating patient details
    serializer = PatientDoctorMappingDoctorOnlySerializer(mappings, many=True)
    
    return Response({
        'patient_details': PatientSerializer(patient).data,
        'doctors': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def mapping_delete(request, pk):
    """
    DELETE: Remove a patient-doctor mapping
    """
    mapping = get_object_or_404(
        PatientDoctorMapping, 
        pk=pk, 
        patient__created_by=request.user
    )
    
    mapping.delete()
    return Response({
        'message': 'Patient-doctor mapping removed successfully'
    }, status=status.HTTP_204_NO_CONTENT)
