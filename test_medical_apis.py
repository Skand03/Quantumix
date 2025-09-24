#!/usr/bin/env python3
"""
Test script for medical API endpoints
"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8001"

def test_endpoint(endpoint, method='GET', data=None, files=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            if files:
                response = requests.post(url, data=data, files=files, timeout=5)
            else:
                headers = {'Content-Type': 'application/json'} if data else {}
                response = requests.post(url, json=data, headers=headers, timeout=5)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text[:200]}...")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint}: Error - {str(e)}")
        return False

def main():
    print("🧪 Testing Medical API Endpoints\n")
    
    # Test page endpoints
    page_endpoints = [
        "/",
        "/xray-upload/",
        "/doctor-panel/",
        "/medical-dashboard/",
        "/future-scope/",
        "/impact/",
    ]
    
    # Test API endpoints
    api_endpoints = [
        "/api/sensor-data/",
        "/api/emergency-stop/",
    ]
    
    # Test medical APIs with POST data
    medical_api_tests = [
        {
            'endpoint': '/api/xray-analysis/',
            'method': 'POST',
            'data': {
                'patient_id': 'test123',
                'image_path': '/test/path/xray.jpg'
            }
        },
        {
            'endpoint': '/api/save-prescription/',
            'method': 'POST', 
            'data': {
                'patient_id': 'test123',
                'prescription': 'Test prescription',
                'doctor_name': 'Dr. Test'
            }
        },
        {
            'endpoint': '/api/generate-report/',
            'method': 'POST',
            'data': {
                'patient_id': 'test123',
                'report_type': 'comprehensive'
            }
        }
    ]
    
    success_count = 0
    total_count = 0
    
    print("📄 Testing Page Endpoints:")
    for endpoint in page_endpoints:
        total_count += 1
        if test_endpoint(endpoint):
            success_count += 1
    
    print("\n🔌 Testing API Endpoints:")
    for endpoint in api_endpoints:
        total_count += 1
        if test_endpoint(endpoint):
            success_count += 1
    
    print("\n🏥 Testing Medical API Endpoints:")
    for test_data in medical_api_tests:
        total_count += 1
        if test_endpoint(test_data['endpoint'], test_data['method'], test_data['data']):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{total_count} endpoints working")
    print(f"✅ Success Rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 All medical features are working correctly!")
    else:
        print(f"\n⚠️  {total_count - success_count} endpoints need attention.")

if __name__ == "__main__":
    main()