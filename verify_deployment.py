#!/usr/bin/env python3
"""
Deployment verification script for AI Wellness Assistant
Tests the application's core functionality after deployment
"""

import requests
import sys
import time
from datetime import datetime

def test_endpoint(url, description, expected_status=200, timeout=10):
    """Test a single endpoint"""
    try:
        print(f"🔍 Testing {description}...")
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == expected_status:
            print(f"  ✅ {description} - OK (Status: {response.status_code})")
            return True
        else:
            print(f"  ❌ {description} - Failed (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {description} - Connection failed: {str(e)}")
        return False

def test_api_endpoint(url, description, method='GET', data=None):
    """Test API endpoints"""
    try:
        print(f"🔍 Testing {description}...")
        
        if method == 'POST':
            response = requests.post(url, json=data, timeout=10)
        else:
            response = requests.get(url, timeout=10)
            
        if response.status_code in [200, 201]:
            print(f"  ✅ {description} - OK")
            return True
        else:
            print(f"  ❌ {description} - Failed (Status: {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {description} - Failed: {str(e)}")
        return False

def main():
    """Main verification function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <base_url>")
        print("Example: python verify_deployment.py http://localhost:5000")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("🧪 AI Wellness Assistant - Deployment Verification")
    print("=" * 55)
    print(f"🎯 Testing deployment at: {base_url}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Wait a moment for the service to be ready
    print("⏳ Waiting for service to be ready...")
    time.sleep(5)
    
    tests_passed = 0
    total_tests = 0
    
    # Test basic endpoints
    endpoints = [
        (f"{base_url}/", "Main dashboard"),
        (f"{base_url}/health", "Health check"),
    ]
    
    for url, description in endpoints:
        total_tests += 1
        if test_endpoint(url, description):
            tests_passed += 1
    
    # Test API endpoints
    api_tests = [
        (f"{base_url}/api/summary", "Summary API", 'GET', None),
        (f"{base_url}/api/track", "Track API", 'POST', {
            'habit': 'water',
            'value': 1,
            'unit': 'glasses',
            'notes': 'Test tracking'
        }),
        (f"{base_url}/api/advice", "Advice API", 'POST', {
            'question': 'How much water should I drink?'
        }),
        (f"{base_url}/api/symptoms", "Symptoms API", 'POST', {
            'description': 'Test symptom check'
        }),
    ]
    
    for url, description, method, data in api_tests:
        total_tests += 1
        if test_api_endpoint(url, description, method, data):
            tests_passed += 1
    
    print()
    print("📊 Test Results")
    print("=" * 20)
    print(f"✅ Passed: {tests_passed}/{total_tests}")
    print(f"❌ Failed: {total_tests - tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print()
        print("🎉 All tests passed! Deployment is successful!")
        print("🌐 Your AI Wellness Assistant is ready to use!")
        sys.exit(0)
    else:
        print()
        print("⚠️  Some tests failed. Please check the deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
