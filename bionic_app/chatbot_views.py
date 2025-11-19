"""
Chatbot API Views
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .chatbot_ai import chatbot


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """Handle chat requests"""
    try:
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({
                'success': False,
                'error': 'No question provided'
            }, status=400)
        
        # Enhanced context about bionic hand project
        context = """
        BIONIC HAND PROJECT SPECIFICATIONS:
        
        CONTROL SYSTEM:
        - Myoelectric control using EMG (electromyography) sensors
        - MyoWare EMG sensor (0.1-5mV signal detection, 1000x amplification)
        - Signal processing: bandpass filter (20-500Hz), rectification, smoothing
        - Arduino Uno microcontroller (ATmega328P, 16MHz, 6 PWM pins)
        - Response latency: <100ms for natural control
        
        HARDWARE COMPONENTS:
        - 5x SG90 micro servos (9g, 4.8-6V, 1.2kg/cm torque, 180° rotation)
        - 3D printed structure: PLA/ABS/PETG (layer height 0.2mm, 20-30% infill)
        - Fishing line tendons (50lb test monofilament)
        - LiPo battery 7.4V 2200mAh (4-6 hours runtime)
        - Voltage regulator 5V for Arduino
        
        CAPABILITIES:
        - 5-10 grip patterns: power grip, precision pinch, tripod, hook, open hand
        - Proportional control based on EMG signal strength
        - 70-90% natural hand function restoration
        - Customizable for different hand sizes (child to adult)
        
        FEATURES:
        - Real-time 2D and 3D simulation modes
        - Individual finger control with realistic joint rotation
        - Machine learning for gesture recognition (SVM, Neural Networks)
        - Firebase cloud storage for research files and data
        - Web-based control interface
        
        COST & ACCESSIBILITY:
        - DIY build cost: $150-500 (vs $5,000-$100,000 commercial)
        - Open-source design and code
        - 3D printable components (15-30 hours print time)
        - Assembly time: 2-3 weeks
        - User training: 2-4 weeks for proficiency
        
        TECHNICAL SPECIFICATIONS:
        - EMG sampling rate: 1000Hz
        - Servo PWM frequency: 50Hz (1-2ms pulse width)
        - Finger closing time: 0.5-1 second
        - Maximum grip force: 6kg (with SG90 servos)
        - Weight: 400-600g (depending on materials)
        """
        
        # Get AI response
        result = chatbot.chat(question, context)
        
        return JsonResponse({
            'success': result['success'],
            'response': result['response'],
            'provider': result['provider']
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'response': "Sorry, I encountered an error. Please try again."
        }, status=500)


@require_http_methods(["GET"])
def chatbot_status(request):
    """Get chatbot AI provider status"""
    status = chatbot.get_status()
    
    return JsonResponse({
        'success': True,
        'status': status,
        'message': f"{status['total_providers']} AI provider(s) available"
    })
