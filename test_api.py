#!/usr/bin/env python3
"""
Simple API test script to verify the healthcare backend is working
Run this after starting the server with: python manage.py runserver
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_user_registration():
    """Test user registration"""
    url = f"{BASE_URL}/api/auth/register/"
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!",
        "password_confirm": "TestPass123!"
    }
    
    response = requests.post(url, json=data)
    print(f"Registration: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ User registered: {result['user']['name']}")
        return result['tokens']['access']
    else:
        print(f"❌ Registration failed: {response.text}")
        return None

def test_user_login():
    """Test user login"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "email": "test@example.com",
        "password": "TestPass123!"
    }
    
    response = requests.post(url, json=data)
    print(f"Login: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ User logged in: {result['user']['name']}")
        return result['tokens']['access']
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_create_doctor(token):
    """Test creating a doctor"""
    url = f"{BASE_URL}/api/doctors/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Dr. John Smith",
        "email": "dr.smith@hospital.com",
        "phone": "+1-555-0123",
        "specialization": "Cardiology",
        "qualification": "MD, FACC",
        "experience_years": 10,
        "license_number": "MD123456",
        "hospital_affiliation": "Test Hospital",
        "consultation_fee": "200.00",
        "is_available": True
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Create Doctor: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Doctor created: {result['data']['name']}")
        return result['data']['id']
    else:
        print(f"❌ Doctor creation failed: {response.text}")
        return None

def test_create_patient(token):
    """Test creating a patient"""
    url = f"{BASE_URL}/api/patients/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "+1-555-0456",
        "date_of_birth": "1990-01-01",
        "gender": "F",
        "address": "123 Test St, Test City, TC 12345",
        "medical_history": "No known allergies"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Create Patient: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Patient created: {result['data']['name']}")
        return result['data']['id']
    else:
        print(f"❌ Patient creation failed: {response.text}")
        return None

def test_assign_doctor_to_patient(token, patient_id, doctor_id):
    """Test assigning a doctor to a patient"""
    url = f"{BASE_URL}/api/mappings/"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "patient": patient_id,
        "doctor": doctor_id,
        "notes": "Initial consultation"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Assign Doctor: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Doctor assigned to patient")
        return result['data']['id']
    else:
        print(f"❌ Doctor assignment failed: {response.text}")
        return None

def test_get_patients(token):
    """Test getting all patients"""
    url = f"{BASE_URL}/api/patients/"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    print(f"Get Patients: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Retrieved {result['count']} patients")
        return True
    else:
        print(f"❌ Get patients failed: {response.text}")
        return False

def main():
    """Main test function"""
    print("🏥 Healthcare Backend API Test")
    print("=" * 40)
    
    # Test registration
    token = test_user_registration()
    if not token:
        # Try login if registration fails (user might already exist)
        token = test_user_login()
        if not token:
            print("❌ Cannot authenticate user")
            sys.exit(1)
    
    print()
    
    # Test creating a doctor
    doctor_id = test_create_doctor(token)
    if not doctor_id:
        print("❌ Cannot create doctor")
        sys.exit(1)
    
    # Test creating a patient
    patient_id = test_create_patient(token)
    if not patient_id:
        print("❌ Cannot create patient")
        sys.exit(1)
    
    # Test assigning doctor to patient
    mapping_id = test_assign_doctor_to_patient(token, patient_id, doctor_id)
    if not mapping_id:
        print("❌ Cannot assign doctor to patient")
        sys.exit(1)
    
    # Test getting patients
    if not test_get_patients(token):
        print("❌ Cannot retrieve patients")
        sys.exit(1)
    
    print()
    print("🎉 All tests passed! The API is working correctly.")
    print("\nYou can now:")
    print("1. Visit http://localhost:8000/admin/ for admin interface")
    print("2. Use the API endpoints with proper authentication")
    print("3. Check the API_TESTING_GUIDE.md for detailed examples")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the server.")
        print("Make sure the Django server is running: python manage.py runserver")
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")