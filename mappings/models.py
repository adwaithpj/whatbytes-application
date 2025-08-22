from django.db import models

class PatientDoctorMapping(models.Model):
    """
    Model to manage patient-doctor relationships
    """
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='patient_mappings')
    assigned_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('patient', 'doctor')
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.patient.name} -> Dr. {self.doctor.name}"
