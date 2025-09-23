from django.http import JsonResponse
import random

def sensor_data(request):
    """Returns dummy IoT sensor data for the bionic hand"""
    data = {
        "flex_sensor": [random.randint(0, 90) for _ in range(5)],  # 5 fingers
        "emg_signal": random.randint(100, 500),
        "grip_force": random.randint(0, 100),
        "temperature": random.uniform(25.0, 40.0),
        "hand_status": random.choice(["Open", "Closing", "Closed"])
    }
    return JsonResponse(data)
