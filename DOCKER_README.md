# Docker Setup for Healthcare Backend

This guide will help you run the Healthcare Backend application using Docker with a PostgreSQL database.

## 🐳 What's Included

- **Django Application**: Your healthcare backend API
- **PostgreSQL Database**: Production-ready database server
- **pgAdmin**: Web-based PostgreSQL administration tool (optional)

## 📋 Prerequisites

- Docker installed on your system
- Docker Compose installed (usually comes with Docker Desktop)

## 🚀 Quick Start

### 1. Clone and Navigate

```bash
cd your-project-directory
```

### 2. Build and Start Services

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

### 3. Access Your Application

- **Django API**: http://localhost:8000
- **pgAdmin** (Database Admin): http://localhost:5050
  - Email: `admin@healthcare.com`
  - Password: `admin123`

## 🔧 Configuration

### Environment Variables

The application uses the following configuration:

- **Database**: PostgreSQL running in Docker
- **Database URL**: `postgresql://postgres:postgres123@db:5432/healthcare_db`
- **Debug Mode**: Enabled for development
- **Admin User**: Automatically created
  - Email: `admin@healthcare.com`
  - Password: `admin123`

### Custom Environment

To customize the configuration:

1. Copy `docker.env` to `.env`
2. Modify the values as needed
3. Restart the containers

## 📊 Database Access

### Using pgAdmin

1. Go to http://localhost:5050
2. Login with admin credentials
3. Add a new server:
   - **Name**: Healthcare DB
   - **Host**: `db`
   - **Port**: `5432`
   - **Username**: `postgres`
   - **Password**: `postgres123`

### Direct PostgreSQL Access

```bash
# Connect to PostgreSQL container
docker exec -it whatbytes-db-1 psql -U postgres -d healthcare_db
```

## 🛠️ Common Commands

### Start Services

```bash
# Start all services
docker-compose up

# Start specific service
docker-compose up web
docker-compose up db
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: This deletes database data)
docker-compose down -v
```

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web
```

### Database Operations

```bash
# Run Django migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Open Django shell
docker-compose exec web python manage.py shell

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Rebuild Application

```bash
# Rebuild only the web service
docker-compose build web

# Rebuild and restart
docker-compose up --build web
```

## 🔍 Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

### Application Issues

```bash
# Check application logs
docker-compose logs web

# Access container shell
docker-compose exec web bash

# Restart application
docker-compose restart web
```

### Port Conflicts

If you get port conflicts, modify the ports in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000" # Change from 8000:8000
```

## 📁 Project Structure

```
├── Dockerfile              # Django app container definition
├── docker-compose.yml      # Multi-service orchestration
├── requirements.txt        # Python dependencies
├── docker.env             # Environment configuration template
├── init-db.sql            # Database initialization script
├── .dockerignore          # Files to exclude from Docker build
└── manage.py              # Django management script
```

## 🔒 Security Notes

**For Production:**

1. Change default passwords in `docker.env`
2. Set `DEBUG=False`
3. Use environment variables for secrets
4. Configure proper networking
5. Set up SSL/TLS
6. Use secrets management

## 🚀 API Endpoints

Once running, your API will be available at:

- Base URL: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Documentation: Check your urls.py for available endpoints

## 💾 Data Persistence

Database data is persisted in Docker volumes:

- `postgres_data`: PostgreSQL database files
- `pgadmin_data`: pgAdmin configuration

To backup your data:

```bash
# Backup database
docker-compose exec db pg_dump -U postgres healthcare_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres healthcare_db < backup.sql
```

## 🛑 Stopping Everything

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers, and delete volumes (DELETES ALL DATA)
docker-compose down -v

# Stop, remove containers, networks, and unused images
docker-compose down --rmi all
```
