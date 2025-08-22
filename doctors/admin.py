from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'specialization', 'experience_years', 'is_available', 'created_at')
    list_filter = ('specialization', 'is_available', 'experience_years', 'created_at')
    search_fields = ('name', 'email', 'specialization', 'license_number')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
