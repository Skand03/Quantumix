from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
import uuid

# Patient Model
class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=15)
    address = models.TextField()
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.patient_id}"
    
    class Meta:
        ordering = ['-created_at']

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    doctor_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField(validators=[MinValueValidator(0)])
    hospital_affiliation = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"
    
    class Meta:
        ordering = ['user__last_name']

# Bionic Device Model
class BionicDevice(models.Model):
    DEVICE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('emergency_stop', 'Emergency Stop'),
    ]
    
    DEVICE_TYPE = [
        ('precision', 'Precision Model'),
        ('standard', 'Standard Model'),
        ('lightweight', 'Lightweight Model'),
        ('comfort_plus', 'Comfort Plus Model'),
        ('athletic', 'Athletic Performance Model'),
    ]
    
    device_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='devices')
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE)
    model_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    firmware_version = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=DEVICE_STATUS, default='inactive')
    battery_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    last_maintenance = models.DateField(null=True, blank=True)
    installation_date = models.DateField()
    warranty_expiry = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.device_type} - {self.serial_number} ({self.patient.user.get_full_name()})"
    
    class Meta:
        ordering = ['-created_at']

# Sensor Reading Model
class SensorReading(models.Model):
    device = models.ForeignKey(BionicDevice, on_delete=models.CASCADE, related_name='sensor_readings')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # EMG Signals (Electromyography)
    emg_signal = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    
    # Grip Force
    grip_force = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Individual Finger Sensors (Flex Sensors)
    thumb_flex = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    index_flex = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    middle_flex = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    ring_flex = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    pinky_flex = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    
    # Temperature
    temperature = models.FloatField(validators=[MinValueValidator(20), MaxValueValidator(45)])
    
    # Pressure Sensors
    palm_pressure = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Accelerometer Data (for gesture detection)
    accel_x = models.FloatField(null=True, blank=True)
    accel_y = models.FloatField(null=True, blank=True)
    accel_z = models.FloatField(null=True, blank=True)
    
    # Gyroscope Data
    gyro_x = models.FloatField(null=True, blank=True)
    gyro_y = models.FloatField(null=True, blank=True)
    gyro_z = models.FloatField(null=True, blank=True)
    
    # Battery Status
    battery_level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Device Status
    is_calibrated = models.BooleanField(default=True)
    error_code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Reading {self.timestamp} - Device {self.device.device_id}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['device', '-timestamp']),
        ]

# Medical Record Model
class MedicalRecord(models.Model):
    RECORD_TYPE = [
        ('xray', 'X-Ray'),
        ('mri', 'MRI'),
        ('ct_scan', 'CT Scan'),
        ('blood_test', 'Blood Test'),
        ('emg_test', 'EMG Test'),
        ('general', 'General Checkup'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='medical_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_path = models.FileField(upload_to='medical_records/', null=True, blank=True)
    
    # Analysis Results
    ai_analysis = models.JSONField(null=True, blank=True)
    fracture_detected = models.BooleanField(default=False)
    bone_density = models.CharField(max_length=20, blank=True, null=True)
    arthritis_detected = models.BooleanField(default=False)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.record_type} - {self.patient.user.get_full_name()} - {self.created_at.date()}"
    
    class Meta:
        ordering = ['-created_at']

# Prescription Model
class Prescription(models.Model):
    prescription_id = models.CharField(max_length=20, unique=True, default=uuid.uuid4)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    
    diagnosis = models.TextField()
    medications = models.JSONField()  # Store as list of medication objects
    instructions = models.TextField()
    follow_up_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Prescription {self.prescription_id} - {self.patient.user.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']

# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()} - {self.appointment_date}"
    
    class Meta:
        ordering = ['appointment_date']

# Analytics Model
class DeviceAnalytics(models.Model):
    device = models.ForeignKey(BionicDevice, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    # Usage Statistics
    total_usage_hours = models.FloatField(default=0)
    active_usage_hours = models.FloatField(default=0)
    grip_count = models.IntegerField(default=0)
    average_grip_force = models.FloatField(default=0)
    
    # Performance Metrics
    response_time_ms = models.FloatField(default=0)  # Average response time
    accuracy_percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    
    # Error Statistics
    error_count = models.IntegerField(default=0)
    emergency_stops = models.IntegerField(default=0)
    
    # Battery Statistics
    charge_cycles = models.IntegerField(default=0)
    average_battery_life = models.FloatField(default=0)  # in hours
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Analytics {self.date} - Device {self.device.device_id}"
    
    class Meta:
        ordering = ['-date']
        unique_together = ['device', 'date']

# Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPE = [
        ('maintenance', 'Maintenance Required'),
        ('battery_low', 'Low Battery'),
        ('error', 'Error Alert'),
        ('appointment', 'Appointment Reminder'),
        ('prescription', 'Prescription Update'),
        ('report', 'New Report Available'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.notification_type} - {self.user.username} - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
