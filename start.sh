#!/bin/bash
# PiRouter Pro - Startup Script
# Requires root privileges

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="/var/lib/pirouter"

echo "🚀 Starting PiRouter Pro..."

# Create data directory
mkdir -p "$APP_DIR"

# Initialize database
python3 "$SCRIPT_DIR/init_db.py"

# Start the app
cd "$SCRIPT_DIR"
exec sudo python3 app.py
