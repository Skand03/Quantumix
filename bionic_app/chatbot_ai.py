"""
AI Chatbot Integration
Supports multiple AI providers: Gemini (Google), OpenAI, Hugging Face
"""

import os
import json
import requests
import time
from django.conf import settings
from django.core.cache import cache


class GeminiAI:
    """Google Gemini AI (FREE and RECOMMENDED)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.enabled = bool(self.api_key)
    
    def chat(self, question, context=""):
        """Generate response using Gemini AI with rate limit handling"""
        if not self.enabled:
            return None
        
        # Check cache first
        cache_key = f"gemini_chat_{hash(question)}"
        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response
        
        # Check rate limit
        rate_limit_key = "gemini_rate_limit"
        if cache.get(rate_limit_key):
            print("Gemini rate limit active, skipping...")
            return None
        
        try:
            # Prepare enhanced prompt with detailed context
            prompt = f"""You are a highly knowledgeable AI assistant specializing in bionic hand prosthetics, biomedical engineering, and assistive technology.

PROJECT SPECIFICATIONS:
{context}

YOUR EXPERTISE:
• EMG Signal Processing: Amplification (1000x), bandpass filtering (20-500Hz), rectification, smoothing, threshold detection
• Myoelectric Control: Pattern recognition, proportional control, multi-grip systems
• Hardware: Arduino Uno (ATmega328P), SG90 servos (1.2kg/cm torque), MyoWare EMG sensors (0.1-5mV)
• 3D Printing: PLA/ABS/PETG materials, 0.2mm layer height, 20-30% infill, FDM printing
• Machine Learning: SVM, Neural Networks, Random Forest for gesture classification (90-95% accuracy)
• Cost Analysis: DIY $150-500 vs Commercial $5,000-$100,000+
• Assembly & Calibration: Step-by-step procedures, troubleshooting, maintenance

USER QUESTION: "{question}"

RESPONSE GUIDELINES:
1. For bionic hand topics: Provide accurate, detailed technical answers with specific numbers, specifications, and examples
2. Use proper formatting: Break into paragraphs, use bullet points for lists, include technical specifications
3. For off-topic questions: Politely redirect to bionic hand topics
4. Be precise, educational, and professional
5. Include relevant technical details (voltages, frequencies, materials, costs, etc.)

Provide a well-formatted, accurate response:"""
            
            # API request with correct format
            url = f"{self.base_url}?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,  # Lower for more accurate, consistent responses
                    "maxOutputTokens": 500,  # Allow comprehensive detailed answers
                    "topP": 0.85,  # Higher for more diverse vocabulary
                    "topK": 40,
                    "candidateCount": 1
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    # Cache successful response for 5 minutes
                    cache.set(cache_key, text, 300)
                    return text
                else:
                    print(f"Gemini unexpected response format: {result}")
                    return None
            elif response.status_code == 429:
                # Rate limit hit - cache for 60 seconds
                print("Gemini rate limit exceeded, caching for 60s")
                cache.set(rate_limit_key, True, 60)
                return None
            else:
                print(f"Gemini API error {response.status_code}: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"Gemini error: {e}")
            return None


class OpenAIChat:
    """OpenAI GPT (Paid but high quality)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.enabled = bool(self.api_key)
    
    def chat(self, question, context=""):
        """Generate response using OpenAI"""
        if not self.enabled:
            return None
        
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": f"You are a helpful research assistant for a bionic hand project. {context}"},
                    {"role": "user", "content": question}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return None
                
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None


class HuggingFaceChat:
    """Hugging Face (FREE)"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.enabled = bool(self.api_key)
    
    def chat(self, question, context=""):
        """Generate response using Hugging Face"""
        if not self.enabled:
            return None
        
        try:
            url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
            headers = {'Authorization': f'Bearer {self.api_key}'}
            data = {"inputs": question}
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                return result[0]['generated_text']
            else:
                return None
                
        except Exception as e:
            print(f"HuggingFace error: {e}")
            return None


class SmartChatbot:
    """Smart chatbot that tries multiple AI providers"""
    
    def __init__(self):
        # Initialize all providers
        self.gemini = GeminiAI()
        self.openai = OpenAIChat()
        self.huggingface = HuggingFaceChat()
        
        # Check which providers are available
        self.providers = []
        if self.gemini.enabled:
            self.providers.append(('Gemini AI', self.gemini))
        if self.openai.enabled:
            self.providers.append(('OpenAI', self.openai))
        if self.huggingface.enabled:
            self.providers.append(('Hugging Face', self.huggingface))
    
    def chat(self, question, context=""):
        """Try to get response from available AI providers"""
        
        # Try each provider in order
        for provider_name, provider in self.providers:
            try:
                response = provider.chat(question, context)
                if response:
                    return {
                        'success': True,
                        'response': response,
                        'provider': provider_name
                    }
            except Exception as e:
                print(f"{provider_name} failed: {e}")
                continue
        
        # If no AI provider works, use fallback
        return {
            'success': False,
            'response': self.fallback_response(question),
            'provider': 'Fallback'
        }
    
    def format_response(self, text):
        """Format response with proper HTML structure"""
        # Add line breaks for better readability
        text = text.replace('\n\n', '<br><br>')
        text = text.replace('\n', '<br>')
        return text
    
    def fallback_response(self, question):
        """Enhanced fallback responses with improved pattern matching and formatting"""
        q = question.lower().strip()
        
        # Remove common punctuation for better matching
        q = q.replace('?', '').replace('!', '').replace('.', '')
        
        # Comprehensive responses for various topics
        
        # AI Model and system questions (check this FIRST before other patterns)
        if 'model' in q and any(word in q for word in ['which', 'what', 'ai', 'use', 'using']):
            return """I'm powered by Google's Gemini AI (gemini-pro model) with intelligent fallback responses. When Gemini API is available, I provide dynamic AI-generated answers with 95%+ accuracy. When rate limits are reached, I use comprehensive pre-programmed responses covering 30+ bionic hand topics. This hybrid approach ensures you always get helpful, detailed answers about EMG signals, control systems, 3D printing, components, and more!"""
        
        # Applications and usage
        elif any(word in q for word in ['where', 'who', 'use', 'application', 'used', 'apply']):
            if 'bionic' in q or 'prosthetic' in q or 'hand' in q:
                return """**Bionic hands are used by:**
1) **Amputees** (2+ million worldwide) - congenital limb difference, accidents, disease
2) **Military veterans** - combat injuries, IED blasts
3) **Industrial workers** - machinery accidents, electrical injuries
4) **Medical patients** - diabetes complications, cancer, infections

**Applications:** Daily living (eating, dressing, writing), work tasks (typing, tool use, assembly), sports/recreation (cycling, gaming), social interaction (handshakes, gestures).

**Locations:** Homes, workplaces, schools, rehabilitation centers, sports facilities. Modern bionic hands restore 70-90% of natural hand function."""
            elif 'emg' in q:
                return """**EMG sensors are used in:**
1) **Prosthetic control** - bionic hands/arms (primary application)
2) **Rehabilitation** - stroke recovery, muscle therapy monitoring
3) **Sports science** - athlete performance, fatigue analysis
4) **Medical diagnosis** - neuromuscular disorders, nerve damage
5) **Human-computer interfaces** - gesture control, VR/AR
6) **Robotics** - exoskeletons, assistive devices

In bionic hands: EMG sensors (typically MyoWare or Advancer Technologies) detect 0.1-5mV signals from forearm muscles, amplify them 1000x, and process them to control 5 servo motors for finger movements."""
        
        # Bionic hand basics
        elif (any(phrase in q for phrase in ['what is', 'what are', 'define', 'explain', 'tell me about']) and 
              any(word in q for word in ['bionic', 'prosthetic', 'artificial hand'])):
            return """<strong>A bionic hand is an advanced electromechanical prosthetic device</strong> that replicates natural hand function through myoelectric control.

<strong>🔧 How It Works:</strong>
• EMG sensors detect muscle signals (0.1-5mV) from residual limb
• Arduino microcontroller processes signals in real-time (<100ms latency)
• 5 servo motors actuate fingers through tendon system
• User controls hand by contracting specific muscle groups

<strong>💪 Capabilities:</strong>
• 5-10 grip patterns: power grip, precision pinch, tripod, hook, open hand
• Proportional control based on signal strength
• 70-90% natural hand function restoration
• Customizable for different hand sizes

<strong>⚙️ Key Components:</strong>
• 3D printed structure (PLA/ABS/PETG)
• 5x SG90 servo motors (1.2kg/cm torque)
• MyoWare EMG sensor (1000x amplification)
• Arduino Uno (ATmega328P, 16MHz)
• LiPo battery 7.4V 2200mAh (4-6 hours)
• Fishing line tendons (50lb test)

<strong>💰 Cost Comparison:</strong>
• DIY Build: $150-500
• Commercial: $5,000-$100,000+

Modern bionic hands enable users to perform daily tasks, work activities, and regain independence with intuitive muscle-based control."""
        
        # How it works
        elif (any(word in q for word in ['how', 'work', 'function', 'operate', 'mechanism']) and 
              any(word in q for word in ['bionic', 'prosthetic', 'hand', 'emg'])):
            return """<strong>🤖 Bionic Hand Operation (Myoelectric Control System):</strong>

<strong>Step 1️⃣ - Signal Detection:</strong>
• EMG sensors placed on forearm skin detect muscle electrical activity
• Signals generated: 0.1-5mV when muscles contract
• Sampling rate: 1000Hz for accurate capture

<strong>Step 2️⃣ - Signal Processing:</strong>
• <strong>Amplification:</strong> 1000x gain (0.1mV → 100mV)
• <strong>Bandpass Filter:</strong> 20-500Hz (removes 50/60Hz noise, motion artifacts)
• <strong>Rectification:</strong> Convert to absolute values
• <strong>Smoothing:</strong> Moving average filter (window: 50-100ms)
• <strong>Threshold Detection:</strong> 30-70% of maximum voluntary contraction

<strong>Step 3️⃣ - Control Logic:</strong>
• Arduino reads processed analog signals (0-1023 ADC values)
• Pattern recognition algorithm identifies intended movement
• Determines grip type: open/close, pinch, power grip, etc.
• Maps signal strength to proportional control

<strong>Step 4️⃣ - Actuation:</strong>
• Arduino sends PWM signals (50Hz, 1-2ms pulse width) to servos
• 5 servo motors pull fishing line tendons
• Fingers move with 0.5-1 second closing time
• Maximum grip force: 6kg with SG90 servos

<strong>Step 5️⃣ - User Feedback:</strong>
• Visual feedback: User sees hand movement
• Proprioceptive feedback: Muscle tension awareness
• User adjusts contraction for precise control

<strong>⏱️ Performance:</strong>
• Response latency: <100ms (feels natural)
• Training time: 2-4 weeks for proficiency
• Accuracy: 90-95% with machine learning"""
        
        # EMG signals
        elif 'emg' in q:
            if 'process' in q or 'filter' in q:
                return """EMG signal processing involves: 1) Amplification (signals are very weak, 0.1-5mV), 2) Filtering (remove noise using bandpass filters 20-500Hz), 3) Rectification (convert to absolute values), 4) Smoothing (moving average), 5) Threshold detection (determine when muscle is active). This clean signal is then used to control the prosthetic."""
            else:
                return """EMG (Electromyography) signals are electrical potentials generated by muscle cells when they contract. In bionic hands, surface EMG sensors placed on the skin detect these signals (typically 0.1-5mV) from residual limb muscles. The signals are amplified, filtered, and processed to determine the user's intended hand movements."""
        
        # Control systems
        elif 'control' in q or 'algorithm' in q:
            if 'machine learning' in q or 'ml' in q or 'ai' in q:
                return """Machine learning enhances bionic hand control by: 1) Training on user's EMG patterns for different gestures, 2) Using classification algorithms (SVM, Neural Networks) to recognize intentions, 3) Adapting to user's muscle patterns over time, 4) Enabling more natural, intuitive control with multiple grip patterns. Our system can learn 5-10 different hand positions."""
            else:
                return """Bionic hand control systems use threshold-based or pattern recognition algorithms. Threshold control: simple on/off based on signal strength. Pattern recognition: analyzes EMG signal features (amplitude, frequency) to classify intended movements. Advanced systems use PID control for smooth, proportional finger movements and can switch between multiple grip patterns."""
        
        # 3D printing
        elif '3d print' in q or 'print' in q:
            if 'material' in q or 'filament' in q:
                return """Best 3D printing materials for bionic hands: 1) PLA - easy to print, biodegradable, good for prototypes, 2) ABS - stronger, heat-resistant, better for functional parts, 3) PETG - combines strength and flexibility, 4) TPU - flexible material for joints and grips. Layer height: 0.2mm, infill: 20-30% for strength vs weight balance."""
            elif 'setting' in q or 'parameter' in q:
                return """Recommended 3D printing settings: Layer height: 0.2mm, Infill: 20-30%, Print speed: 50mm/s, Nozzle temp: 200-220°C (PLA), Bed temp: 60°C, Supports: Yes for overhangs >45°, Wall thickness: 3-4 perimeters. Print fingers vertically for better strength along the length."""
            else:
                return """3D printing makes bionic hands affordable and customizable. The hand is designed in CAD software (Fusion 360, SolidWorks), then sliced and printed in parts: fingers, palm, wrist, forearm socket. Total print time: 15-30 hours. After printing, parts are assembled with servos, tendons (fishing line), and electronics. Cost: $50-100 in materials."""
        
        # Components and hardware
        elif 'component' in q or 'part' in q or 'hardware' in q:
            if 'servo' in q or 'motor' in q:
                return """Servo motors for bionic hands: SG90 micro servos (9g, $2 each) for fingers - need 5 servos. Specs: 4.8-6V, 180° rotation, 1.2kg/cm torque. Alternative: MG90S (metal gear, more durable). Servos connect to Arduino PWM pins and are controlled via PWM signals (1-2ms pulse width). Position feedback allows precise finger control."""
            elif 'sensor' in q:
                return """Key sensors: 1) EMG sensors (MyoWare, $40) - detect muscle signals, 2) Flex sensors ($10) - measure finger bend for feedback, 3) Force sensors (FSR, $7) - detect grip pressure, 4) IMU (MPU6050, $5) - track hand orientation. Sensors connect to Arduino analog pins and provide real-time feedback for control."""
            elif 'arduino' in q or 'microcontroller' in q:
                return """Arduino Uno ($25) is the brain of the bionic hand. It has: 14 digital I/O pins (6 PWM for servos), 6 analog inputs (for EMG/sensors), 16MHz processor, 32KB memory. The Arduino reads EMG signals, runs control algorithms, and sends PWM signals to servos. Alternative: Arduino Nano (smaller) or ESP32 (WiFi/Bluetooth)."""
            else:
                return """Essential components: 1) Arduino Uno ($25) - microcontroller, 2) 5x SG90 servos ($10) - finger actuation, 3) MyoWare EMG sensor ($40) - muscle signal detection, 4) LiPo battery 7.4V ($20) - power supply, 5) 3D printed parts ($50) - structure, 6) Fishing line ($5) - tendons, 7) Velcro straps ($5) - attachment. Total: $150-200."""
        
        # Cost and budget
        elif 'cost' in q or 'price' in q or 'budget' in q or 'expensive' in q or 'cheap' in q:
            return """DIY bionic hand costs: Basic version: $150-200 (Arduino, basic EMG, simple servos), Advanced version: $300-500 (better sensors, metal gear servos, battery management), Commercial prosthetics: $5,000-$100,000+. Our open-source approach makes functional prosthetics accessible. Most expensive parts: EMG sensors ($40-100) and servos ($10-50)."""
        
        # Assembly and building
        elif 'build' in q or 'assemble' in q or 'make' in q or 'construct' in q:
            return """Building steps: 1) 3D print all parts (15-30 hours), 2) Assemble fingers with servos and tendons, 3) Wire Arduino to servos and EMG sensors, 4) Upload control code to Arduino, 5) Calibrate EMG thresholds, 6) Test each finger movement, 7) Create custom socket for user's limb, 8) Train user on muscle control patterns. Total time: 2-3 weeks."""
        
        # Programming and code
        elif 'code' in q or 'program' in q or 'software' in q or 'arduino' in q:
            return """Arduino code structure: 1) Setup: initialize servos, EMG pins, serial communication, 2) Loop: read EMG values, apply filtering, check thresholds, map to servo positions, 3) Functions: calibration, grip patterns (pinch, power, tripod), smooth movement. Libraries used: Servo.h for motor control. Code is open-source on our GitHub."""
        
        # Calibration
        elif 'calibrat' in q or 'tune' in q or 'adjust' in q:
            return """Calibration process: 1) Baseline: measure EMG when muscles are relaxed, 2) Maximum: measure EMG during strong contraction, 3) Set thresholds: typically 30-70% of maximum, 4) Test movements: verify each finger responds correctly, 5) Fine-tune: adjust sensitivity and response time. Recalibrate weekly as user adapts. Takes 10-15 minutes."""
        
        # Grip patterns
        elif 'grip' in q or 'grasp' in q or 'gesture' in q:
            return """Common grip patterns: 1) Power grip - all fingers curl (holding bottles), 2) Precision pinch - thumb + index (picking small objects), 3) Tripod grip - thumb + index + middle (writing), 4) Hook grip - fingers curl, thumb extended (carrying bags), 5) Open hand - all fingers extended (releasing objects). Users switch grips via muscle co-contraction."""
        
        # Machine learning
        elif 'machine learning' in q or 'neural network' in q or 'deep learning' in q:
            return """Machine learning for bionic hands: 1) Collect EMG data for different gestures (100+ samples each), 2) Extract features (RMS, frequency, wavelength), 3) Train classifier (SVM, Random Forest, or Neural Network), 4) Achieve 90-95% accuracy, 5) Real-time prediction (<100ms latency). This enables intuitive control of 5-10 different hand positions."""
        
        # Battery and power
        elif 'battery' in q or 'power' in q:
            return """Power system: LiPo battery 7.4V 2200mAh ($20) provides 4-6 hours of use. Servos draw 100-500mA each (500-2500mA total). Include voltage regulator (5V for Arduino), low-voltage cutoff protection, and charging circuit. Alternative: 6x AA batteries (cheaper but heavier). Add power switch and LED indicator. Charge time: 2-3 hours."""
        
        # Materials and durability
        elif 'material' in q or 'durable' in q or 'strong' in q or 'break' in q:
            return """Material selection: Fingers: ABS or PETG (strong, impact-resistant), Joints: TPU (flexible), Palm: PLA or ABS (rigid structure), Socket: PETG (comfortable, strong). Durability: properly printed parts last 1-2 years with daily use. Weak points: tendon attachment points (reinforce with metal inserts), servo gears (use metal gear servos for heavy use)."""
        
        # Comparison with commercial
        elif 'commercial' in q or 'professional' in q or 'compare' in q:
            return """DIY vs Commercial: DIY ($150-500): customizable, repairable, open-source, good for learning, 80% functionality. Commercial ($5k-100k): FDA approved, waterproof, better sensors, warranty, professional fitting, 95% functionality. Our DIY approach provides functional prosthetics at 1-5% of commercial cost, ideal for developing countries and education."""
        
        # Sensors and feedback
        elif 'feedback' in q or 'feel' in q or 'sensation' in q:
            return """Sensory feedback options: 1) Vibration motors - provide tactile feedback when gripping, 2) Force sensors - measure grip strength, 3) Visual feedback - LED indicators, 4) Audio feedback - beeps for different states. Advanced: haptic feedback systems that stimulate nerves. Basic vibration feedback adds $10-20 to cost and significantly improves control."""
        
        # Maintenance
        elif 'maintain' in q or 'repair' in q or 'fix' in q:
            return """Maintenance: 1) Weekly: check tendon tension, clean sensors, charge battery, 2) Monthly: lubricate servo gears, inspect 3D printed parts for cracks, recalibrate EMG, 3) Common repairs: replace broken tendons ($2), swap failed servos ($2-5), reprint damaged fingers ($3). Keep spare parts on hand. Average maintenance: 1 hour/month."""
        
        # Training and learning
        elif 'train' in q or 'learn' in q or 'practice' in q:
            return """User training: Week 1: Learn to activate EMG sensors with muscle contractions, Week 2: Practice basic open/close movements, Week 3: Master grip switching, Week 4: Perform daily tasks (eating, writing). Training games help: squeeze ball, pick up objects, stack blocks. Most users achieve functional control in 2-4 weeks with 30 min daily practice."""
        
        # Wireless and connectivity
        elif 'wireless' in q or 'bluetooth' in q or 'wifi' in q:
            return """Wireless options: 1) Bluetooth (HC-05 module, $5) - connect to smartphone app for settings, 2) WiFi (ESP32, $10) - cloud data logging, remote monitoring, 3) Advantages: no wires, easier donning/doffing, smartphone control. Disadvantage: battery drain. Bluetooth adds 10-15% battery consumption but greatly improves user experience."""
        
        # Safety
        elif 'safe' in q or 'danger' in q or 'risk' in q:
            return """Safety considerations: 1) Electrical: use proper insulation, voltage regulation, avoid water exposure, 2) Mechanical: limit servo torque to prevent injury, add soft padding on grip surfaces, 3) Biological: hypoallergenic materials for skin contact, clean sensors regularly, 4) Emergency: include manual release mechanism, power cutoff switch. Follow safety guidelines for medical devices."""
        
        # Customization
        elif 'custom' in q or 'personalize' in q or 'modify' in q:
            return """Customization options: 1) Size: scale 3D model to fit user (child to adult), 2) Color: print in any filament color, add paint/decals, 3) Features: add extra sensors, LED lights, different grip patterns, 4) Aesthetics: realistic skin-tone covers or futuristic designs, 5) Socket: custom-fitted to residual limb. Each hand is unique to the user's needs and preferences."""
        
        # Research and development
        elif 'research' in q or 'future' in q or 'advance' in q:
            return """Current research areas: 1) Targeted muscle reinnervation (TMR) - surgical technique for better EMG signals, 2) Osseointegration - direct bone attachment, 3) Sensory feedback - nerve stimulation for touch sensation, 4) AI control - deep learning for natural movements, 5) Soft robotics - flexible, safer prosthetics. Future: fully integrated, thought-controlled bionic hands with sensation."""
        
        # Getting started
        elif 'start' in q or 'begin' in q or 'first' in q:
            return """Getting started: 1) Learn basics: Arduino programming, 3D printing, electronics, 2) Get tools: 3D printer (or use service), soldering iron, multimeter, 3) Order components: see our Components page, 4) Download files: 3D models and code from our GitHub, 5) Join community: forums, Discord for help. Start with simple Arduino + servo project before full hand. Estimated learning time: 1-2 months."""
        
        # General questions
        elif 'hello' in q or 'hi' in q or 'hey' in q:
            return """Hello! I'm your bionic hand research assistant. I can help you with EMG signal processing, control systems, 3D printing techniques, component selection, assembly instructions, programming, and more. What would you like to know about building bionic hands?"""
        
        elif 'thank' in q:
            return """You're welcome! Feel free to ask if you have more questions about bionic hands, prosthetics, or our project. Happy building!"""
        
        # Off-topic detection
        elif any(word in q for word in ['java', 'python', 'javascript', 'weather', 'news', 'sports', 'movie', 'music', 'game']):
            # Check if it's actually about programming for bionic hands
            if any(word in q for word in ['arduino', 'code', 'program', 'bionic', 'prosthetic', 'emg']):
                return """For bionic hand programming, we use **Arduino C/C++** (not Java/Python). The Arduino IDE compiles C++ code for the ATmega328P microcontroller. Key libraries: Servo.h for motor control, analogRead() for EMG sensors. If you want to add Python for machine learning (gesture recognition), you can use: scikit-learn for classification, PySerial for Arduino communication, NumPy for signal processing. Would you like specific code examples?"""
            else:
                return """I specialize in **bionic hand prosthetics and biomedical engineering**. I can't help with that topic, but I'd love to discuss:

**🔬 Technical:** EMG signal processing, control algorithms, machine learning for gesture recognition
**⚙️ Hardware:** Arduino, servos, sensors, 3D printing, electronic components  
**🔧 Building:** Assembly, calibration, testing, troubleshooting, maintenance
**💰 Practical:** Cost optimization ($150-500), customization, user training

Try asking: "how does EMG work?", "what components do I need?", or "how to build a bionic hand?"."""
        
        # Default response with suggestions
        else:
            return """I'm your bionic hand expert! I can help with:

**🔬 Technical Topics:**
- EMG signal processing & filtering (bandpass, rectification, smoothing)
- Control algorithms (threshold, pattern recognition, PID)
- Machine learning (SVM, neural networks for gesture classification)
- Arduino programming (C++, Servo.h, PWM control)

**⚙️ Hardware & Components:**
- Servos (SG90, MG90S specs & selection)
- Sensors (MyoWare EMG, flex, force, IMU)
- 3D printing (PLA/ABS/PETG materials, settings)
- Power systems (LiPo batteries, voltage regulation)

**🔧 Building & Assembly:**
- Step-by-step construction guide
- Calibration procedures
- Testing & troubleshooting
- Maintenance & repairs

**💰 Practical Information:**
- Cost breakdown ($150-500 DIY)
- Customization options
- User training (2-4 weeks)
- Safety considerations

**Ask me anything!** Examples: "how does EMG work?", "what components do I need?", "how to calibrate?", "3D printing settings?"."""
    
    def get_status(self):
        """Get status of AI providers"""
        return {
            'gemini': self.gemini.enabled,
            'openai': self.openai.enabled,
            'huggingface': self.huggingface.enabled,
            'total_providers': len(self.providers)
        }


# Initialize global chatbot instance
chatbot = SmartChatbot()
