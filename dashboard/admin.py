from django.contrib import admin
from .models import (
    Patient, Doctor, BionicDevice, SensorReading,
    MedicalRecord, Prescription, Appointment,
    DeviceAnalytics, Notification
)

# Patient Admin
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'user', 'gender', 'blood_type', 'phone_number', 'created_at']
    list_filter = ['gender', 'blood_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'patient_id', 'phone_number']
    date_hierarchy = 'created_at'

# Doctor Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['doctor_id', 'user', 'specialization', 'license_number', 'years_of_experience']
    list_filter = ['specialization', 'years_of_experience']
    search_fields = ['user__username', 'doctor_id', 'license_number']

# Bionic Device Admin
@admin.register(BionicDevice)
class BionicDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'patient', 'device_type', 'status', 'battery_level', 'installation_date']
    list_filter = ['device_type', 'status', 'installation_date']
    search_fields = ['device_id', 'serial_number', 'patient__user__username']
    date_hierarchy = 'installation_date'

# Sensor Reading Admin
@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ['device', 'timestamp', 'emg_signal', 'grip_force', 'battery_level']
    list_filter = ['timestamp', 'is_calibrated']
    search_fields = ['device__device_id']
    date_hierarchy = 'timestamp'

# Medical Record Admin
@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'record_type', 'fracture_detected', 'confidence_score', 'created_at']
    list_filter = ['record_type', 'fracture_detected', 'arthritis_detected', 'created_at']
    search_fields = ['patient__user__username', 'doctor__user__username', 'title']
    date_hierarchy = 'created_at'

# Prescription Admin
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['prescription_id', 'patient', 'doctor', 'created_at']
    list_filter = ['created_at']
    search_fields = ['prescription_id', 'patient__user__username', 'doctor__user__username']
    date_hierarchy = 'created_at'

# Appointment Admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__user__username', 'doctor__user__username']
    date_hierarchy = 'appointment_date'

# Device Analytics Admin
@admin.register(DeviceAnalytics)
class DeviceAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['device', 'date', 'total_usage_hours', 'accuracy_percentage', 'error_count']
    list_filter = ['date']
    search_fields = ['device__device_id']
    date_hierarchy = 'date'

# Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'created_at'
