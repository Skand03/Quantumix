"""
URL Configuration for Bionic Hand System App
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('components/', views.components, name='components'),
    path('circuit/', views.circuit, name='circuit'),
    path('simulation/', views.simulation, name='simulation'),
    path('simulation-3d/', views.simulation_3d, name='simulation_3d'),
    path('simulation-3d-advanced/', views.simulation_3d_advanced, name='simulation_3d_advanced'),
    path('research/', views.research, name='research'),
    path('progress/', views.progress, name='progress'),
    path('contact/', views.contact, name='contact'),
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
]
