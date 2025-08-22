from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone', 'date_of_birth', 
            'gender', 'address', 'medical_history', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def validate_email(self, value):
        """
        Validate email uniqueness for the current user's patients
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            queryset = Patient.objects.filter(created_by=user, email=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    "A patient with this email already exists in your records."
                )
        return value

class PatientCreateSerializer(PatientSerializer):
    """
    Serializer for creating patients
    """
    pass

class PatientUpdateSerializer(PatientSerializer):
    """
    Serializer for updating patients
    """
    pass