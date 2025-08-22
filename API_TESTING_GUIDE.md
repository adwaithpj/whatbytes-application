# Healthcare Backend API Testing Guide

This guide provides comprehensive examples for testing all API endpoints using Postman or any HTTP client.

## Base URL

```
http://localhost:8000
```

## Authentication Flow

### 1. Register a New User

```http
POST /api/auth/register/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
}
```

**Expected Response:**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "date_joined": "2024-01-01T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### 2. Login User

```http
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
}
```

**Expected Response:**

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "date_joined": "2024-01-01T10:00:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

## Patient Management APIs

**Note:** All patient endpoints require authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### 3. Create a Patient

```http
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1-555-0123",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "123 Main Street, Anytown, ST 12345",
    "medical_history": "No known allergies. Previous surgery: appendectomy in 2015."
}
```

**Expected Response:**

```json
{
  "message": "Patient created successfully",
  "data": {
    "id": 1,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1-555-0123",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "123 Main Street, Anytown, ST 12345",
    "medical_history": "No known allergies. Previous surgery: appendectomy in 2015.",
    "created_by": "john.doe@example.com",
    "created_at": "2024-01-01T10:30:00Z",
    "updated_at": "2024-01-01T10:30:00Z"
  }
}
```

### 4. Get All Patients (for authenticated user)

```http
GET /api/patients/
Authorization: Bearer <access_token>
```

**Expected Response:**

```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "phone": "+1-555-0123",
      "date_of_birth": "1990-05-15",
      "gender": "F",
      "address": "123 Main Street, Anytown, ST 12345",
      "medical_history": "No known allergies. Previous surgery: appendectomy in 2015.",
      "created_by": "john.doe@example.com",
      "created_at": "2024-01-01T10:30:00Z",
      "updated_at": "2024-01-01T10:30:00Z"
    }
  ]
}
```

### 5. Get Specific Patient

```http
GET /api/patients/1/
Authorization: Bearer <access_token>
```

### 6. Update Patient

```http
PUT /api/patients/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Jane Smith-Johnson",
    "email": "jane.smith@example.com",
    "phone": "+1-555-0123",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "456 Oak Avenue, Newtown, ST 12345",
    "medical_history": "No known allergies. Previous surgery: appendectomy in 2015. Recent checkup: all normal."
}
```

### 7. Delete Patient

```http
DELETE /api/patients/1/
Authorization: Bearer <access_token>
```

**Expected Response:**

```json
{
  "message": "Patient deleted successfully"
}
```

## Doctor Management APIs

### 8. Create a Doctor

```http
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Dr. Michael Johnson",
    "email": "dr.johnson@hospital.com",
    "phone": "+1-555-0456",
    "specialization": "Cardiology",
    "qualification": "MD, FACC",
    "experience_years": 15,
    "license_number": "MD123456789",
    "hospital_affiliation": "City General Hospital",
    "consultation_fee": "250.00",
    "is_available": true
}
```

**Expected Response:**

```json
{
  "message": "Doctor created successfully",
  "data": {
    "id": 1,
    "name": "Dr. Michael Johnson",
    "email": "dr.johnson@hospital.com",
    "phone": "+1-555-0456",
    "specialization": "Cardiology",
    "qualification": "MD, FACC",
    "experience_years": 15,
    "license_number": "MD123456789",
    "hospital_affiliation": "City General Hospital",
    "consultation_fee": "250.00",
    "is_available": true,
    "created_at": "2024-01-01T11:00:00Z",
    "updated_at": "2024-01-01T11:00:00Z"
  }
}
```

### 9. Get All Doctors

```http
GET /api/doctors/
Authorization: Bearer <access_token>
```

### 10. Get Specific Doctor

```http
GET /api/doctors/1/
Authorization: Bearer <access_token>
```

### 11. Update Doctor

```http
PUT /api/doctors/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Dr. Michael Johnson",
    "email": "dr.johnson@hospital.com",
    "phone": "+1-555-0456",
    "specialization": "Cardiology",
    "qualification": "MD, FACC",
    "experience_years": 16,
    "license_number": "MD123456789",
    "hospital_affiliation": "City General Hospital",
    "consultation_fee": "275.00",
    "is_available": true
}
```

### 12. Delete Doctor

```http
DELETE /api/doctors/1/
Authorization: Bearer <access_token>
```

## Patient-Doctor Mapping APIs

### 13. Assign Doctor to Patient

```http
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient": 1,
    "doctor": 1,
    "notes": "Regular cardiology checkup scheduled for next month."
}
```

**Expected Response:**

```json
{
  "message": "Patient-doctor mapping created successfully",
  "data": {
    "id": 1,
    "patient": 1,
    "doctor": 1,
    "patient_details": {
      "id": 1,
      "name": "Jane Smith",
      "email": "jane.smith@example.com",
      "phone": "+1-555-0123",
      "date_of_birth": "1990-05-15",
      "gender": "F",
      "address": "123 Main Street, Anytown, ST 12345",
      "medical_history": "No known allergies. Previous surgery: appendectomy in 2015.",
      "created_by": "john.doe@example.com",
      "created_at": "2024-01-01T10:30:00Z",
      "updated_at": "2024-01-01T10:30:00Z"
    },
    "doctor_details": {
      "id": 1,
      "name": "Dr. Michael Johnson",
      "email": "dr.johnson@hospital.com",
      "phone": "+1-555-0456",
      "specialization": "Cardiology",
      "qualification": "MD, FACC",
      "experience_years": 15,
      "license_number": "MD123456789",
      "hospital_affiliation": "City General Hospital",
      "consultation_fee": "250.00",
      "is_available": true,
      "created_at": "2024-01-01T11:00:00Z",
      "updated_at": "2024-01-01T11:00:00Z"
    },
    "assigned_date": "2024-01-01T12:00:00Z",
    "notes": "Regular cardiology checkup scheduled for next month.",
    "is_active": true
  }
}
```

### 14. Get All Patient-Doctor Mappings

```http
GET /api/mappings/
Authorization: Bearer <access_token>
```

### 15. Get All Doctors for a Specific Patient

```http
GET /api/mappings/1/
Authorization: Bearer <access_token>
```

**Expected Response:**

```json
{
    "patient": "Jane Smith",
    "doctors": [
        {
            "id": 1,
            "patient": 1,
            "doctor": 1,
            "patient_details": { ... },
            "doctor_details": { ... },
            "assigned_date": "2024-01-01T12:00:00Z",
            "notes": "Regular cardiology checkup scheduled for next month.",
            "is_active": true
        }
    ]
}
```

### 16. Remove Doctor from Patient

```http
DELETE /api/mappings/delete/1/
Authorization: Bearer <access_token>
```

**Expected Response:**

```json
{
  "message": "Patient-doctor mapping removed successfully"
}
```

## Error Responses

### Authentication Errors

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Validation Errors

```json
{
  "email": ["A patient with this email already exists in your records."],
  "password": [
    "This password is too short. It must contain at least 8 characters."
  ]
}
```

### Permission Errors

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found Errors

```json
{
  "detail": "Not found."
}
```

## Postman Collection Setup

1. **Create a new collection** called "Healthcare Backend API"

2. **Set up environment variables:**

   - `base_url`: `http://localhost:8000`
   - `access_token`: (will be set after login)

3. **Add a pre-request script for authenticated endpoints:**

   ```javascript
   if (pm.request.url.path.join("/").includes("auth") === false) {
     pm.request.headers.add({
       key: "Authorization",
       value: "Bearer " + pm.environment.get("access_token"),
     });
   }
   ```

4. **Add a test script for login endpoints to save the token:**
   ```javascript
   if (pm.response.code === 200 || pm.response.code === 201) {
     var jsonData = pm.response.json();
     if (jsonData.tokens && jsonData.tokens.access) {
       pm.environment.set("access_token", jsonData.tokens.access);
     }
   }
   ```

## Testing Workflow

1. **Register a new user** or **Login** to get access tokens
2. **Create some doctors** using the doctor endpoints
3. **Create some patients** using the patient endpoints
4. **Assign doctors to patients** using the mapping endpoints
5. **Test all CRUD operations** for each resource type
6. **Test error cases** (invalid data, unauthorized access, etc.)

## Security Features Tested

- ✅ JWT Authentication required for protected endpoints
- ✅ Users can only access their own patient records
- ✅ Email uniqueness validation
- ✅ Password strength validation
- ✅ Proper error handling and messages
- ✅ CORS configuration for frontend integration

## Database Schema

The API uses the following main models:

- **User**: Custom user model with email authentication
- **Patient**: Patient records linked to users
- **Doctor**: Doctor profiles (shared across users)
- **PatientDoctorMapping**: Many-to-many relationship between patients and doctors

All timestamps are automatically managed, and soft deletes can be implemented by setting `is_active=False` on mappings.
