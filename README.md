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

### 🐳 Option 1: Docker (Recommended for Development)

Docker provides the easiest way to get started with the Healthcare Backend API. It automatically sets up PostgreSQL database and all dependencies.

1. **Prerequisites**

   - Install [Docker](https://www.docker.com/get-started) and Docker Compose

2. **Clone the repository**

   ```bash
   git clone https://github.com/adwaithpj/whatbytes-application.git
   cd healthcare-backend
   ```

3. **Start with Docker**

   ```bash
   # Build and start all services (Django + PostgreSQL + pgAdmin)
   docker-compose up --build

   # Or run in background
   docker-compose up --build -d
   ```

4. **Access your application**

   - **API**: http://localhost:8000
   - **Admin Panel**: http://localhost:8000/admin/
     - Email: `admin@healthcare.com`
     - Password: `admin123`
   - **pgAdmin** (Database UI): http://localhost:5050
     - Email: `admin@healthcare.com`
     - Password: `admin123`

5. **That's it!** 🎉
   The application automatically:
   - Sets up PostgreSQL database
   - Runs all migrations
   - Creates a superuser account
   - Starts the Django development server

### ⚙️ Option 2: Manual Installation

If you prefer to set up the environment manually:

1. **Clone the repository**

   ```bash
   git clone https://github.com/adwaithpj/whatbytes-application.git
   cd healthcare-backend
   ```

2. **Create virtual environment**

   ```bash
   python -m venv whatbytes
   source whatbytes/bin/activate  # On Windows: whatbytes\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root:

   ```env
   # Option 1: Use full PostgreSQL URL (Recommended)
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/healthcare_db

   # Option 2: Individual database variables
   # DB_NAME=healthcare_db
   # DB_USER=postgres
   # DB_PASSWORD=your_password
   # DB_HOST=localhost
   # DB_PORT=5432

   # Django Configuration
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Database Setup**

   - Install and start PostgreSQL
   - Create database named `healthcare_db`
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

## 🐳 Docker Commands

### Common Docker Operations

```bash
# Start services
docker-compose up                    # Start and view logs
docker-compose up -d                 # Start in background
docker-compose up --build            # Rebuild and start

# Stop services
docker-compose down                  # Stop all services
docker-compose down -v              # Stop and remove volumes (⚠️ Deletes database data)

# View logs
docker-compose logs                  # View all logs
docker-compose logs web              # View Django app logs
docker-compose logs db               # View PostgreSQL logs
docker-compose logs -f               # Follow logs in real-time

# Database operations
docker-compose exec web python manage.py migrate                # Run migrations
docker-compose exec web python manage.py createsuperuser        # Create additional superuser
docker-compose exec web python manage.py shell                  # Open Django shell
docker-compose exec db psql -U postgres -d healthcare_db        # Connect to PostgreSQL directly

# Container management
docker-compose ps                    # View running containers
docker-compose restart web           # Restart Django app
docker-compose build web            # Rebuild Django app container
```

### Docker Troubleshooting

**Port conflicts:**

```bash
# If port 8000 is already in use, modify docker-compose.yml:
ports:
  - "8001:8000"  # Use port 8001 instead
```

**Database connection issues:**

```bash
# Check if database is running
docker-compose ps
docker-compose logs db

# Reset database completely
docker-compose down -v
docker-compose up --build
```

**View application in real-time:**

```bash
# The Docker setup includes volume mounting, so changes to your code
# will automatically reload the Django development server
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
├── Dockerfile             # Docker container definition
├── docker-compose.yml     # Multi-service Docker orchestration
├── entrypoint.sh          # Docker container startup script
├── init-db.sql           # PostgreSQL initialization script
├── .dockerignore         # Files to exclude from Docker build
├── docker.env            # Docker environment configuration template
├── requirements.txt       # Python dependencies
├── DOCKER_README.md       # Detailed Docker setup guide
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
