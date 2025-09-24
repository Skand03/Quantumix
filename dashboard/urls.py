from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('test-functionality/', views.test_functionality_view, name='test_functionality'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('control/', views.control_view, name='control'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    
    # New Medical Features
    path('xray-upload/', views.xray_upload_view, name='xray_upload'),
    path('doctor-panel/', views.doctor_panel_view, name='doctor_panel'),
    path('medical-dashboard/', views.medical_dashboard_view, name='medical_dashboard'),
    path('future-scope/', views.future_scope_view, name='future_scope'),
    path('impact/', views.impact_view, name='impact'),
    
    # API endpoints
    path('api/sensor-data/', views.sensor_data_api, name='sensor_data_api'),
    path('api/emergency-stop/', views.emergency_stop_api, name='emergency_stop_api'),
    path('api/device-control/', views.device_control_api, name='device_control_api'),
    
    # Medical API endpoints
    path('api/xray-analysis/', views.xray_analysis_api, name='xray_analysis_api'),
    path('api/save-prescription/', views.save_prescription_api, name='save_prescription_api'),
    path('api/generate-report/', views.generate_report_api, name='generate_report_api'),
]
