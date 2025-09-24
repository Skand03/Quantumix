from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json

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
