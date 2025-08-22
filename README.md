# Healthcare Backend API

A comprehensive healthcare management system built with Django REST Framework, featuring JWT authentication and PostgreSQL database.

## Features

- **User Authentication**: JWT-based authentication system
- **Patient Management**: CRUD operations for patient records
- **Doctor Management**: CRUD operations for doctor profiles
- **Patient-Doctor Mapping**: Assign and manage patient-doctor relationships
- **Secure API**: Authentication-protected endpoints
- **PostgreSQL Database**: Robust data storage

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **Additional**: CORS headers, Python Decouple for environment variables

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/adwaithpj/whatbytes-application.git
   cd healthcare-backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv whatbytes
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root with the following variables:

   ```env
   # Database Configuration
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432

   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**

   - Create PostgreSQL database named `healthcare_db`
   - Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication APIs

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user and get JWT tokens

### Patient Management APIs

- `GET /api/patients/` - Get all patients (authenticated user's patients)
- `POST /api/patients/` - Create a new patient
- `GET /api/patients/<id>/` - Get specific patient details
- `PUT /api/patients/<id>/` - Update patient details
- `DELETE /api/patients/<id>/` - Delete patient record

### Doctor Management APIs

- `GET /api/doctors/` - Get all doctors
- `POST /api/doctors/` - Create a new doctor
- `GET /api/doctors/<id>/` - Get specific doctor details
- `PUT /api/doctors/<id>/` - Update doctor details
- `DELETE /api/doctors/<id>/` - Delete doctor record

### Patient-Doctor Mapping APIs

- `GET /api/mappings/` - Get all patient-doctor mappings
- `POST /api/mappings/` - Assign a doctor to a patient
- `GET /api/mappings/<patient_id>/` - Get all doctors for a specific patient
- `DELETE /api/mappings/delete/<id>/` - Remove doctor from patient

## API Usage Examples

### Register User

```bash
POST /api/auth/register/
Content-Type: application/json

{
    "name": "John Doe",
    "email": "john@example.com",
    "username": "johndoe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
```

### Login User

```bash
POST /api/auth/login/
Content-Type: application/json

{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

### Create Patient (Authenticated)

```bash
POST /api/patients/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1234567890",
    "date_of_birth": "1990-05-15",
    "gender": "F",
    "address": "123 Main St, City, State",
    "medical_history": "No known allergies"
}
```

### Create Doctor (Authenticated)

```bash
POST /api/doctors/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "name": "Dr. Smith",
    "email": "dr.smith@hospital.com",
    "phone": "+1234567891",
    "specialization": "Cardiology",
    "qualification": "MD, MBBS",
    "experience_years": 10,
    "license_number": "LIC123456",
    "hospital_affiliation": "City Hospital",
    "consultation_fee": "200.00",
    "is_available": true
}
```

### Assign Doctor to Patient (Authenticated)

```bash
POST /api/mappings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "patient": 1,
    "doctor": 1,
    "notes": "Regular checkup scheduled"
}
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. After successful login, you'll receive:

- `access` token: Valid for 60 minutes
- `refresh` token: Valid for 7 days

Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Data Models

### User Model

- Custom user model with email as username field
- Fields: name, email, username, password

### Patient Model

- Fields: name, email, phone, date_of_birth, gender, address, medical_history
- Linked to user who created the record

### Doctor Model

- Fields: name, email, phone, specialization, qualification, experience_years, license_number, hospital_affiliation, consultation_fee, is_available

### PatientDoctorMapping Model

- Links patients to doctors
- Fields: patient, doctor, assigned_date, notes, is_active

## Security Features

- JWT authentication for all protected endpoints
- Users can only access their own patient records
- Email and license number uniqueness validation
- Password validation using Django's built-in validators
- CORS configuration for frontend integration

## Admin Interface

Access the Django admin interface at `/admin/` to manage:

- Users
- Patients
- Doctors
- Patient-Doctor Mappings

## Testing

You can test the API endpoints using:

- **Postman**: Import the endpoints and test with proper authentication
- **curl**: Command-line testing
- **Django REST Framework Browsable API**: Visit endpoints in browser

## Project Structure

```
healthcare_backend/
├── healthcare_backend/     # Main project settings
├── authentication/        # User authentication app
├── patients/              # Patient management app
├── doctors/               # Doctor management app
├── mappings/              # Patient-doctor mapping app
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
