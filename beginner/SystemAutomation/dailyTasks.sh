#!/bin/bash
# ================================
# Daily Automation Script
# ================================

cd "$HOME/systemAutomation"

echo '=== Running bakcup ==='
./backup.sh

echo "=== Cleaning Logs ==="
./cleanupO7.sh

echo '=== Checking Permissions ==='
./checkPermissions.sh

echo "✅ Daily tasks completed at $(date)"

