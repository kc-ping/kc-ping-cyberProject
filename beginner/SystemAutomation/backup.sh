#!/bin/bash
# ================================
# Backup Script
# Author: Tchemako Nganou Ken-andrew Mael
# Description: Backup important files to /backup folder
# ================================
SOURCE_DIR="$HOME/Documents"
BACKUP_DIR="$HOME/backup"
DATE=$(date +%y-%m-%d)

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "❌ Source directory does not exist: $SOURCE_DIR"
    exit 1
fi

# Copy files and compress them
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" "$SOURCE_DIR"

echo "✅ Backup completed: $BACKUP_DIR/backup_$DATE.tar.gz"
