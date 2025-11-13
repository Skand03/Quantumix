"""
Django Models for Bionic Hand System
These are optional local models for admin use
Main data storage is in Firebase Firestore
"""
from django.db import models
from django.contrib.auth.models import User

class Component(models.Model):
    """Local model for components (optional, main data in Firestore)"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    firestore_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class SimulationLog(models.Model):
    """Local model for simulation logs"""
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=100, default='guest')
    firestore_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} - {self.timestamp}"

class ResearchFile(models.Model):
    """Local model for research files"""
    title = models.CharField(max_length=200)
    file_url = models.URLField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    firestore_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_on']
    
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    """Local model for contact messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    firestore_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name}"

class Progress(models.Model):
    """Local model for project progress timeline"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image_url = models.URLField(blank=True, null=True)
    firestore_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.title
