#!/bin/bash

# Variables
NGINX_CONF_DIR="/etc/nginx"
SITES_AVAILABLE="$NGINX_CONF_DIR/sites-available"
SITES_ENABLED="$NGINX_CONF_DIR/sites-enabled"
CONF_FILE="$SITES_AVAILABLE/messaging_system"
LINK_FILE="$SITES_ENABLED/messaging_system"
PYTHON_APP_PORT=5000

# Create the Nginx configuration file
cat <<EOF | sudo tee $CONF_FILE
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:$PYTHON_APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    error_log /var/log/nginx/messaging_system_error.log;
    access_log /var/log/nginx/messaging_system_access.log;
}
EOF

echo "Created Nginx configuration file at $CONF_FILE"

# Create a symbolic link in sites-enabled
if [ ! -L $LINK_FILE ]; then
    sudo ln -s $CONF_FILE $LINK_FILE
    echo "Created symbolic link to $CONF_FILE in $SITES_ENABLED"
else
    echo "Symbolic link already exists"
fi

# Test the Nginx configuration
if ! sudo nginx -t; then
    echo "Nginx configuration test failed. Exiting."
    exit 1
fi

# Reload Nginx to apply the changes
sudo systemctl reload nginx
echo "Nginx reloaded"

# Print success message
echo "Nginx is now set up to forward port 80 to your Python application on port $PYTHON_APP_PORT"
