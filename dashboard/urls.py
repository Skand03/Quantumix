from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('control/', views.control_view, name='control'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    
    # API endpoints
    path('api/sensor-data/', views.sensor_data_api, name='sensor_data_api'),
    path('api/emergency-stop/', views.emergency_stop_api, name='emergency_stop_api'),
    path('api/device-control/', views.device_control_api, name='device_control_api'),
]
