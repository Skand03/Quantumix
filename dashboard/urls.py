from django.urls import path
from . import views
from .notification_views import (
    NotificationCheckView, DeviceStatusView, BatteryStatusView,
    DeviceReconnectView, NotificationLogView, SystemHealthView,
    ActivityLogView
)
from .seo_utils import generate_sitemap, generate_robots_txt, generate_manifest_json

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('test-functionality/', views.test_functionality_view, name='test_functionality'),
    path('model-testing/', views.model_testing_view, name='model_testing'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('control/', views.control_view, name='control'),
    path('settings/', views.settings_view, name='settings'),
    path('about/', views.about_view, name='about'),
    path('offline/', views.offline_view, name='offline'),
    
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
    
    # Notification API endpoints
    path('api/notifications/check/', NotificationCheckView.as_view(), name='notification_check'),
    path('api/notifications/log/', NotificationLogView.as_view(), name='notification_log'),
    path('api/device-status/', DeviceStatusView.as_view(), name='device_status'),
    path('api/battery-status/', BatteryStatusView.as_view(), name='battery_status'),
    path('api/device/reconnect/', DeviceReconnectView.as_view(), name='device_reconnect'),
    path('api/system-health/', SystemHealthView.as_view(), name='system_health'),
    path('api/activity-log/', ActivityLogView.as_view(), name='activity_log'),
    
    # SEO and PWA endpoints
    path('sitemap.xml', generate_sitemap, name='sitemap'),
    path('robots.txt', generate_robots_txt, name='robots'),
    path('manifest.json', generate_manifest_json, name='manifest'),
]
