from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import random
import json
import base64
import io
from datetime import datetime, timedelta

def test_functionality_view(request):
    """Test page for medical functionality"""
    return render(request, 'dashboard/test_functionality.html')

def model_testing_view(request):
    """AI model testing page for bionic hand detection"""
    return render(request, 'dashboard/model_testing.html')

def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

def analytics_view(request):
    return render(request, "dashboard/analytics.html")

def control_view(request):
    return render(request, "dashboard/control.html")

def settings_view(request):
    return render(request, "dashboard/settings.html")

def about_view(request):
    return render(request, "dashboard/about.html")

# New Medical Features Views
def xray_upload_view(request):
    return render(request, "dashboard/xray_upload.html")

def doctor_panel_view(request):
    return render(request, "dashboard/doctor_panel.html")

def medical_dashboard_view(request):
    return render(request, "dashboard/medical_dashboard.html")

def future_scope_view(request):
    return render(request, "dashboard/future_scope.html")

def impact_view(request):
    return render(request, "dashboard/impact.html")

# API endpoint for real-time sensor data
def sensor_data_api(request):
    # Simulated sensor data for demo purposes
    data = {
        'grip_force': round(random.uniform(0, 100), 1),
        'emg_signal': round(random.uniform(0, 100), 1),
        'temperature': round(random.uniform(36.0, 37.5), 1),
        'battery': round(random.uniform(20, 100), 1),
        'status': random.choice(['Normal', 'Calibrating', 'Charging']),
        'finger_sensors': {
            'thumb': round(random.uniform(0, 100), 1),
            'index': round(random.uniform(0, 100), 1),
            'middle': round(random.uniform(0, 100), 1),
            'ring': round(random.uniform(0, 100), 1),
            'pinky': round(random.uniform(0, 100), 1)
        },
        'timestamp': '2025-01-24 ' + str(random.randint(10, 23)) + ':' + str(random.randint(10, 59)) + ':' + str(random.randint(10, 59))
    }
    return JsonResponse(data)

# API endpoint for emergency stop
@csrf_exempt
def emergency_stop_api(request):
    if request.method == 'POST':
        # In a real application, this would send a stop signal to the bionic hand
        return JsonResponse({'status': 'success', 'message': 'Emergency stop activated'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# API endpoint for device control
@csrf_exempt
def device_control_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            control_type = data.get('type')
            value = data.get('value')
            
            # In a real application, this would send control signals to the device
            return JsonResponse({
                'status': 'success', 
                'message': f'Control command sent: {control_type} = {value}'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Medical AI/ML APIs
@csrf_exempt
def xray_analysis_api(request):
    if request.method == 'POST':
        try:
            # Simulate ML analysis with dummy results
            detection_results = {
                'fracture': {
                    'detected': random.choice([True, False]),
                    'confidence': round(random.uniform(75, 95), 1),
                    'location': random.choice(['Metacarpal', 'Phalanx', 'Radius', 'Ulna']) if random.choice([True, False]) else None
                },
                'bone_density': {
                    'status': random.choice(['Normal', 'Low', 'Very Low']),
                    'confidence': round(random.uniform(80, 98), 1),
                    'recommendation': 'Regular monitoring advised'
                },
                'arthritis': {
                    'detected': random.choice([True, False]),
                    'severity': random.choice(['Mild', 'Moderate', 'Severe']) if random.choice([True, False]) else 'None',
                    'confidence': round(random.uniform(70, 92), 1)
                },
                'overall_score': round(random.uniform(85, 95), 1),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            # Generate recommendations based on results
            recommendations = generate_bionic_hand_recommendation(detection_results)
            
            return JsonResponse({
                'status': 'success',
                'results': detection_results,
                'recommendations': recommendations
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def generate_bionic_hand_recommendation(results):
    """Generate bionic hand recommendations based on ML results"""
    recommendations = []
    
    if results['fracture']['detected']:
        recommendations.append({
            'model': 'Precision Model',
            'reason': 'Advanced sensors for delicate movements during recovery',
            'confidence': 90
        })
    
    if results['bone_density']['status'] in ['Low', 'Very Low']:
        recommendations.append({
            'model': 'Lightweight Model',
            'reason': 'Reduced stress on weakened bone structure',
            'confidence': 85
        })
    
    if results['arthritis']['detected'] and results['arthritis']['severity'] in ['Moderate', 'Severe']:
        recommendations.append({
            'model': 'Comfort Plus Model',
            'reason': 'Enhanced ergonomics for arthritis management',
            'confidence': 88
        })
    
    if not recommendations:
        recommendations.append({
            'model': 'Standard Model',
            'reason': 'No specific conditions detected, standard model recommended',
            'confidence': 92
        })
    
    return recommendations

@csrf_exempt
def save_prescription_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # In a real app, this would save to database
            prescription_data = {
                'patient_id': data.get('patient_id', 'P001'),
                'doctor_name': data.get('doctor_name', 'Dr. Smith'),
                'prescription': data.get('prescription', ''),
                'notes': data.get('notes', ''),
                'timestamp': datetime.now().isoformat(),
                'id': f"PRESC_{random.randint(1000, 9999)}"
            }
            
            return JsonResponse({
                'status': 'success',
                'prescription_id': prescription_data['id'],
                'message': 'Prescription saved successfully'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def generate_report_api(request):
    if request.method == 'POST':
        try:
            # Simulate PDF report generation
            report_data = {
                'report_id': f"RPT_{random.randint(10000, 99999)}",
                'generated_at': datetime.now().isoformat(),
                'patient_info': {
                    'name': 'John Doe',
                    'age': 45,
                    'id': 'P001',
                    'condition': 'Hand amputation - Right hand'
                },
                'analysis_results': {
                    'fracture_detected': random.choice([True, False]),
                    'bone_density': random.choice(['Normal', 'Low']),
                    'recommended_model': 'Precision Model'
                },
                'download_url': f'/api/download-report/{random.randint(1000, 9999)}/'
            }
            
            return JsonResponse({
                'status': 'success',
                'report': report_data,
                'message': 'Report generated successfully'
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
