# 🚀 Deployment Guide - Fruit Quality Detection App

This guide provides comprehensive instructions for deploying the Fruit Quality Detection application in various environments.

## 🏠 Local Development

### Quick Start
```bash
# 1. Navigate to project directory
cd fruit_detection_project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

### Development Features
- **Debug Mode**: Enabled by default (`debug=True`)
- **Hot Reload**: Automatic server restart on file changes
- **Error Pages**: Detailed error information in development
- **Static Files**: Served by Flask development server

## 🌐 Production Deployment

### Option 1: Gunicorn (Recommended)

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Run with Gunicorn
```bash
# Basic command
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With configuration
gunicorn --config gunicorn.conf.py app:app
```

#### Create `gunicorn.conf.py`
```python
# Gunicorn configuration file
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Logging
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "fruit_detection_app"

# Server mechanics
daemon = False
pidfile = "app.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (if using HTTPS)
# keyfile = "path/to/keyfile"
# certfile = "path/to/certfile"
```

### Option 2: uWSGI

#### Install uWSGI
```bash
pip install uwsgi
```

#### Create `uwsgi.ini`
```ini
[uwsgi]
module = app:app
master = true
processes = 4
socket = fruit_detection.sock
chmod-socket = 660
vacuum = true
die-on-term = true
```

#### Run with uWSGI
```bash
uwsgi --ini uwsgi.ini
```

## 🐳 Docker Deployment

### Create `Dockerfile`
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p static/uploads

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Create `docker-compose.yml`
```yaml
version: '3.8'

services:
  fruit-detection:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./static/uploads:/app/static/uploads
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/app/static
    depends_on:
      - fruit-detection
    restart: unless-stopped
```

### Build and Run with Docker
```bash
# Build the image
docker build -t fruit-detection-app .

# Run the container
docker run -d -p 5000:5000 --name fruit-app fruit-detection-app

# Or use Docker Compose
docker-compose up -d
```

## 🔧 Nginx Configuration

### Create `nginx.conf`
```nginx
events {
    worker_connections 1024;
}

http {
    upstream fruit_app {
        server fruit-detection:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        client_max_body_size 16M;

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Application
        location / {
            proxy_pass http://fruit_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
    }

    # HTTPS configuration (optional)
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /path/to/certificate.crt;
        ssl_certificate_key /path/to/private.key;

        # SSL configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;

        client_max_body_size 16M;

        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        location / {
            proxy_pass http://fruit_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

## ☁️ Cloud Deployment

### Heroku Deployment

#### Create `Procfile`
```
web: gunicorn app:app
```

#### Create `runtime.txt`
```
python-3.9.15
```

#### Deploy Steps
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create fruit-detection-app

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Scale the app
heroku ps:scale web=1
```

### AWS EC2 Deployment

#### Instance Setup
1. Launch EC2 instance (Ubuntu 20.04 LTS recommended)
2. Configure security groups (allow ports 22, 80, 443)
3. Connect via SSH

#### Server Configuration
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Clone/upload your application
git clone <repository-url>
cd fruit_detection_project

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/fruit-detection.service
```

#### Systemd Service Configuration
```ini
[Unit]
Description=Fruit Detection Flask App
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/fruit_detection_project
Environment="PATH=/home/ubuntu/fruit_detection_project/venv/bin"
ExecStart=/home/ubuntu/fruit_detection_project/venv/bin/gunicorn --workers 3 --bind unix:fruit-detection.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Start Services
```bash
# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl start fruit-detection
sudo systemctl enable fruit-detection

# Configure Nginx
sudo nano /etc/nginx/sites-available/fruit-detection
sudo ln -s /etc/nginx/sites-available/fruit-detection /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 🔐 Security Considerations

### Production Security Checklist

1. **Environment Variables**
```bash
# Use environment variables for sensitive data
export FLASK_SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"
```

2. **Update Flask Configuration**
```python
import os
from flask import Flask

app = Flask(__name__)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
```

3. **File Upload Security**
- Validate file extensions
- Scan uploaded files for malware
- Limit file sizes
- Store uploads outside web root

4. **HTTPS Configuration**
- Use SSL certificates (Let's Encrypt recommended)
- Redirect HTTP to HTTPS
- Set security headers

### Security Headers (Nginx)
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 📊 Monitoring & Logging

### Application Monitoring

#### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }
```

#### Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/fruit_detection.log',
                                     maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Fruit Detection application startup')
```

## 🚀 Performance Optimization

### Application Level
1. **Model Loading**: Load model once at startup
2. **Image Caching**: Cache processed images
3. **Response Compression**: Enable gzip compression
4. **Static File Serving**: Use CDN for static assets

### Server Level
1. **Worker Processes**: Scale based on CPU cores
2. **Connection Pooling**: Use connection pools for databases
3. **Load Balancing**: Distribute traffic across multiple instances
4. **Caching**: Implement Redis for session storage

### Database Optimization (if added)
```python
# Example with SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fruit_detection.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
db = SQLAlchemy(app)
```

## 🔄 Backup & Recovery

### Automated Backups
```bash
#!/bin/bash
# backup.sh - Daily backup script

DATE=$(date +%Y%m%d)
BACKUP_DIR="/backups/fruit-detection"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files
tar -czf $BACKUP_DIR/app-$DATE.tar.gz /path/to/app

# Backup uploaded files
tar -czf $BACKUP_DIR/uploads-$DATE.tar.gz /path/to/app/static/uploads

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

### Cron Job for Backups
```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancers (HAProxy, AWS ALB)
- Implement session storage (Redis)
- Use shared file storage for uploads (AWS S3)

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize TensorFlow for available hardware
- Use GPU acceleration if available

---

**Note**: This deployment guide provides a comprehensive foundation. Adjust configurations based on your specific requirements and infrastructure constraints.