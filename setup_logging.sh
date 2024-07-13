#!/bin/bash

# Define variables
LOG_DIR="/home/ubuntu"
LOG_FILE="$LOG_DIR/messaging_system.log"
USER="ubuntu"

# Create the log directory if it doesn't exist
if [ ! -d "$LOG_DIR" ]; then
    sudo mkdir -p "$LOG_DIR"
    echo "Created directory $LOG_DIR"
else
    echo "Directory $LOG_DIR already exists"
fi

# Create the log file if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    sudo touch "$LOG_FILE"
    echo "Created file $LOG_FILE"
else
    echo "File $LOG_FILE already exists"
fi

# Change ownership of the log file to the specified user
sudo chown "$USER":"$USER" "$LOG_FILE"
echo "Changed ownership of $LOG_FILE to $USER"

# Change permissions of the log file to be readable and writable by the owner and group
sudo chmod 664 "$LOG_FILE"
echo "Changed permissions of $LOG_FILE to 664"

# Verify changes
ls -l "$LOG_FILE"
