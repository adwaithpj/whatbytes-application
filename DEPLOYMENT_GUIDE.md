# Healthcare Backend Deployment Guide

This guide covers deploying the Healthcare Backend API to production environments.

## Pre-Deployment Checklist

- [ ] PostgreSQL database set up and accessible
- [ ] Environment variables configured
- [ ] Static files configured (if serving frontend)
- [ ] SSL certificate ready (for HTTPS)
- [ ] Domain name configured
- [ ] Firewall rules configured

## Environment Configuration

### 1. Production Environment Variables

Create a `.env` file with production values:

```env
# Database Configuration
DB_NAME=healthcare_production_db
DB_USER=healthcare_user
DB_PASSWORD=your_secure_database_password
DB_HOST=your_db_host
DB_PORT=5432

# Django Configuration
SECRET_KEY=your_super_secure_secret_key_here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Additional Production Settings
DJANGO_SETTINGS_MODULE=healthcare_backend.settings
```

### 2. Generate Secure Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL** on your server
2. **Create database and user**:

```sql
CREATE DATABASE healthcare_production_db;
CREATE USER healthcare_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_production_db TO healthcare_user;
ALTER USER healthcare_user CREATEDB;
```

3. **Update PostgreSQL configuration** (`postgresql.conf` and `pg_hba.conf`) if needed

## Server Deployment Options

### Option 1: Traditional Server (Ubuntu/CentOS)

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and PostgreSQL client
sudo apt install python3 python3-pip python3-venv postgresql-client nginx -y

# Install supervisor for process management
sudo apt install supervisor -y
```

#### 2. Setup Application

```bash
# Create application directory
sudo mkdir -p /var/www/healthcare-backend
cd /var/www/healthcare-backend

# Clone your repository
git clone <your-repo-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Set up environment file
cp .env.template .env
# Edit .env with production values

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files (if needed)
python manage.py collectstatic --noinput
```

#### 3. Configure Gunicorn

Create `/var/www/healthcare-backend/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True
timeout = 30
keepalive = 2
user = "www-data"
group = "www-data"
```

#### 4. Configure Supervisor

Create `/etc/supervisor/conf.d/healthcare-backend.conf`:

```ini
[program:healthcare-backend]
command=/var/www/healthcare-backend/venv/bin/gunicorn --config /var/www/healthcare-backend/gunicorn_config.py healthcare_backend.wsgi:application
directory=/var/www/healthcare-backend
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-backend.log
environment=PATH="/var/www/healthcare-backend/venv/bin"
```

#### 5. Configure Nginx

Create `/etc/nginx/sites-available/healthcare-backend`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/healthcare-backend/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/healthcare-backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/healthcare-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. Start Services

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start healthcare-backend
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn psycopg2-binary

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "healthcare_backend.wsgi:application"]
```

#### 2. Create docker-compose.yml

```yaml
version: "3.8"

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: healthcare_db
      POSTGRES_USER: healthcare_user
      POSTGRES_PASSWORD: your_secure_password
    ports:
      - "5432:5432"

  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_NAME=healthcare_db
      - DB_USER=healthcare_user
      - DB_PASSWORD=your_secure_password
      - DB_HOST=db
      - DB_PORT=5432
      - DEBUG=False
      - SECRET_KEY=your_secret_key_here
    volumes:
      - ./static:/app/static
      - ./media:/app/media

volumes:
  postgres_data:
```

#### 3. Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Option 3: Cloud Deployment (Heroku)

#### 1. Install Heroku CLI and login

```bash
heroku login
```

#### 2. Create Heroku app

```bash
heroku create your-healthcare-app
```

#### 3. Add PostgreSQL addon

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 4. Set environment variables

```bash
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

#### 5. Create Procfile

```
web: gunicorn healthcare_backend.wsgi:application --log-file -
release: python manage.py migrate
```

#### 6. Deploy

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### 7. Create superuser

```bash
heroku run python manage.py createsuperuser
```

## SSL/HTTPS Configuration

### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Production Settings Updates

### Update settings.py for production

```python
# Add to healthcare_backend/settings.py

if not DEBUG:
    # Security settings
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Static files
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_ROOT = BASE_DIR / 'media'

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/var/log/django.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
```

## Monitoring and Maintenance

### 1. Log Monitoring

```bash
# Application logs
sudo tail -f /var/log/healthcare-backend.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# System logs
sudo journalctl -u supervisor -f
```

### 2. Database Backup

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U healthcare_user healthcare_production_db > /backups/healthcare_backup_$DATE.sql
```

### 3. Health Check Endpoint

Add to your Django app:

```python
# In any views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "healthy", "timestamp": timezone.now()})
```

### 4. Monitoring with Uptime Checks

Set up monitoring services like:

- UptimeRobot
- Pingdom
- StatusCake
- New Relic

## Security Best Practices

1. **Keep dependencies updated**

   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Regular security scans**

   ```bash
   pip install safety
   safety check
   ```

3. **Firewall configuration**

   ```bash
   sudo ufw allow ssh
   sudo ufw allow 'Nginx Full'
   sudo ufw enable
   ```

4. **Regular backups**
5. **Monitor logs for suspicious activity**
6. **Use strong passwords and 2FA**
7. **Keep server OS updated**

## Troubleshooting

### Common Issues

1. **Database connection errors**

   - Check PostgreSQL is running
   - Verify connection credentials
   - Check firewall rules

2. **Static files not loading**

   - Run `collectstatic` command
   - Check Nginx configuration
   - Verify file permissions

3. **502 Bad Gateway**

   - Check Gunicorn is running
   - Verify Nginx upstream configuration
   - Check application logs

4. **Permission denied errors**
   - Check file ownership: `chown -R www-data:www-data /var/www/healthcare-backend`
   - Check file permissions: `chmod -R 755 /var/www/healthcare-backend`

### Performance Optimization

1. **Database indexing**
2. **Caching with Redis**
3. **CDN for static files**
4. **Database connection pooling**
5. **Gzip compression**

## Scaling Considerations

1. **Load balancing with multiple app servers**
2. **Database read replicas**
3. **Caching layer (Redis/Memcached)**
4. **Horizontal scaling with containers**
5. **Queue system for background tasks (Celery)**

This deployment guide covers the most common deployment scenarios. Choose the option that best fits your infrastructure and requirements.
