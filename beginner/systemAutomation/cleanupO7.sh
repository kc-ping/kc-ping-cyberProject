#!/bin/bash
# ================================
# Cleanup Script
# Description: Delete log files older than 7 days
# ================================

LOG_DIR="/var/log"

# Find and remove old logs
sudo find "$LOG_DIR" -type f -name "*.log" -mtime +7 -exec rm -f {} \;

echo "🧹 Cleanup completed for logs older than 7 days."

