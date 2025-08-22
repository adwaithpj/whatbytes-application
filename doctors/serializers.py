from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model
    """
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone', 'specialization', 
            'qualification', 'experience_years', 'license_number',
            'hospital_affiliation', 'consultation_fee', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_license_number(self, value):
        """
        Validate license number uniqueness
        """
        queryset = Doctor.objects.filter(license_number=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value
    
    def validate_email(self, value):
        """
        Validate email uniqueness
        """
        queryset = Doctor.objects.filter(email=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

class DoctorCreateSerializer(DoctorSerializer):
    """
    Serializer for creating doctors
    """
    pass

class DoctorUpdateSerializer(DoctorSerializer):
    """
    Serializer for updating doctors
    """
    pass