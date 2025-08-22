from rest_framework import serializers
from .models import PatientDoctorMapping

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model
    """
    patient_details = serializers.SerializerMethodField()
    doctor_details = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_details', 'doctor_details',
            'assigned_date', 'notes', 'is_active'
        ]
        read_only_fields = ('id', 'assigned_date')
    
    def get_patient_details(self, obj):
        """Get patient details"""
        from patients.serializers import PatientSerializer
        return PatientSerializer(obj.patient).data
    
    def get_doctor_details(self, obj):
        """Get doctor details"""
        from doctors.serializers import DoctorSerializer
        return DoctorSerializer(obj.doctor).data
    
    def validate(self, attrs):
        """
        Validate that the patient belongs to the current user
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = attrs.get('patient')
            if patient and patient.created_by != request.user:
                raise serializers.ValidationError(
                    "You can only assign doctors to your own patients."
                )
        return attrs

class PatientDoctorMappingCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating patient-doctor mappings
    """
    class Meta:
        model = PatientDoctorMapping
        fields = ['patient', 'doctor', 'notes']
    
    def validate(self, attrs):
        """
        Validate that the patient belongs to the current user and mapping doesn't exist
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            patient = attrs.get('patient')
            doctor = attrs.get('doctor')
            
            if patient and patient.created_by != request.user:
                raise serializers.ValidationError(
                    "You can only assign doctors to your own patients."
                )
            
            # Check if mapping already exists
            if PatientDoctorMapping.objects.filter(
                patient=patient, 
                doctor=doctor, 
                is_active=True
            ).exists():
                raise serializers.ValidationError(
                    "This patient is already assigned to this doctor."
                )
        
        return attrs

class PatientDoctorMappingDoctorOnlySerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping that only includes doctor details
    Used when patient details are already provided at response level
    """
    doctor_details = serializers.SerializerMethodField()
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'doctor', 'doctor_details',
            'assigned_date', 'notes', 'is_active'
        ]
        read_only_fields = ('id', 'assigned_date')
    
    def get_doctor_details(self, obj):
        """Get doctor details"""
        from doctors.serializers import DoctorSerializer
        return DoctorSerializer(obj.doctor).data