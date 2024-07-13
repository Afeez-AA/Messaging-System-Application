# Messaging-System-Application

# Messaging System

This repository contains a Flask-based messaging system with asynchronous task processing using Celery, RabbitMQ, and Redis. Nginx is used as a reverse proxy, and Ngrok provides a secure tunnel to your local development environment.

## Prerequisites

Ensure you have the following software installed on your system:

- Python 3.12
- RabbitMQ
- Redis
- Nginx
- Ngrok

## Setup Instructions

### 1. Install Necessary Dependencies

Update your system and install the required software:

```bash
sudo apt-get update
sudo apt-get install -y rabbitmq-server nginx python3-pip
sudo apt-get install -y redis-server
```
### 2. Set Up RabbitMQ and Redis

```bash
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

sudo systemctl status rabbitmq-server
sudo systemctl status redis-server
```
### 3. Clone the Repository
Create a directory for the project and clone the repository:
```bash
mkdir messaging_system
cd messaging_system
git clone https://github.com/Afeez-AA/Messaging-System-Application.git
cd Messaging-System-Apllication

```

### 4. Create a Python Virtual Environment
Install the virtual environment package and create a virtual environment:

```bash
sudo apt install python3.12-venv
python3 -m venv myprojectenv
source myprojectenv/bin/activate
```
### 5. Install Python Dependencies
Install the required Python packages:
```bash
    pip install -r requirement.txt
```

### 6. Create Nginx Configuration File
Create an Nginx configuration file:
```bash
sudo nano /etc/nginx/sites-available/messaging_system
```
Add the following content to the file:

```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 7. Create a Symbolic Link
Create a symbolic link of your configuration file from sites-available to sites-enabled:
```bash
sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled/

```
### 8. Verify Nginx Configuration
Check the Nginx configuration for syntax errors and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```
### 9.  Install Ngrok
Install Ngrok and configure it with your authtoken:
```bash
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok

ngrok config add-authtoken <your-ngrok-authtoken>
```
### 10. Run the Services
Run the Flask app, Celery worker, and Ngrok in the background:
```bash
nohup python3 app.py &
nohup celery -A celery_app worker --loglevel=info &
nohup ngrok http --domain=blessed-completely-lioness.ngrok-free.app 5000 &
```

# Code Walkthrough

## Flask App (app.py)

### Endpoint /message
- **Handles `sendmail` and `talktome` parameters.**
  - **sendmail**: Queues an email sending task.
  - **talktome**: Logs the current time.

### Asynchronous Processing
- Uses Celery to handle tasks asynchronously.

### Logging
- Tracks requests and errors.

## Celery Setup (celery_app.py and tasks.py)

### Background Tasks
- Celery handles `send_email` and `log_current_time` tasks.

### Redis
- Used as the broker and backend for Celery tasks.

## Ngrok

### Usage
- **ngrok**: Exposes the Flask application to the internet.
- **Domain**: Configured to use a static ngrok domain for consistent URL access.

