from django.db import models

class Doctor(models.Model):
    """
    Doctor model to store doctor information
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    license_number = models.CharField(max_length=100, unique=True)
    hospital_affiliation = models.CharField(max_length=255, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
