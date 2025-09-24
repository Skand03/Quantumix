from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
import time

# Global device state
device_state = {
    "is_running": True,
    "power_level": 85,
    "calibrated": True,
    "emergency_stop": False,
    "last_command_time": time.time()
}

def sensor_data(request):
    """Returns dummy IoT sensor data for the bionic hand"""
    global device_state
    
    # If device is stopped, return static/minimal data
    if not device_state["is_running"] or device_state["emergency_stop"]:
        data = {
            "flex_sensor": [0, 0, 0, 0, 0],  # All fingers at rest
            "emg_signal": 0,
            "grip_force": 0,
            "temperature": 25.0,
            "hand_status": "Stopped",
            "device_state": device_state
        }
        return JsonResponse(data)
    
    # Normal operation - return dynamic sensor data
    data = {
        "flex_sensor": [random.randint(0, 90) for _ in range(5)],  # 5 fingers
        "emg_signal": random.randint(100, 500),
        "grip_force": random.randint(0, 100),
        "temperature": random.uniform(25.0, 40.0),
        "hand_status": random.choice(["Open", "Closing", "Closed"]),
        "device_state": device_state
    }
    return JsonResponse(data)

@csrf_exempt
@require_http_methods(["POST"])
def device_control(request):
    """Handle device control commands"""
    global device_state
    
    try:
        data = json.loads(request.body)
        command = data.get('command')
        
        if command == 'start':
            if device_state["emergency_stop"]:
                return JsonResponse({
                    "success": False, 
                    "message": "Cannot start - Emergency stop is active. Please reset first.",
                    "device_state": device_state
                })
            device_state["is_running"] = True
            device_state["last_command_time"] = time.time()
            return JsonResponse({
                "success": True, 
                "message": "Bionic hand started successfully",
                "device_state": device_state
            })
            
        elif command == 'stop':
            device_state["is_running"] = False
            device_state["last_command_time"] = time.time()
            return JsonResponse({
                "success": True, 
                "message": "Bionic hand stopped successfully",
                "device_state": device_state
            })
            
        elif command == 'emergency_stop':
            device_state["is_running"] = False
            device_state["emergency_stop"] = True
            device_state["last_command_time"] = time.time()
            return JsonResponse({
                "success": True, 
                "message": "Emergency stop activated",
                "device_state": device_state
            })
            
        elif command == 'reset':
            device_state["emergency_stop"] = False
            device_state["is_running"] = False  # Require explicit start after reset
            device_state["last_command_time"] = time.time()
            return JsonResponse({
                "success": True, 
                "message": "System reset completed. Ready to start.",
                "device_state": device_state
            })
            
        elif command == 'calibrate':
            if not device_state["is_running"]:
                return JsonResponse({
                    "success": False, 
                    "message": "Device must be running to calibrate",
                    "device_state": device_state
                })
            device_state["calibrated"] = True
            device_state["last_command_time"] = time.time()
            return JsonResponse({
                "success": True, 
                "message": "Calibration completed successfully",
                "device_state": device_state
            })
            
        else:
            return JsonResponse({
                "success": False, 
                "message": "Unknown command",
                "device_state": device_state
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False, 
            "message": "Invalid JSON data",
            "device_state": device_state
        })
    except Exception as e:
        return JsonResponse({
            "success": False, 
            "message": f"Error: {str(e)}",
            "device_state": device_state
        })
