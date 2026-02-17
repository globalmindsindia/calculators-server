#!/bin/bash

# Fix SQLite database permissions for production server

echo "Fixing database permissions..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Database location
DB_DIR="$SCRIPT_DIR/instance"
DB_FILE="$DB_DIR/unified_database.db"

# Create instance directory if it doesn't exist
mkdir -p "$DB_DIR"

# Set permissions on the instance directory (needs write access for SQLite journal files)
chmod 775 "$DB_DIR"

# Set permissions on the database file if it exists
if [ -f "$DB_FILE" ]; then
    chmod 664 "$DB_FILE"
    echo "Database file permissions updated: $DB_FILE"
else
    echo "Database file not found at: $DB_FILE"
    echo "It will be created automatically when the app runs"
fi

# Change ownership to the web server user (adjust as needed)
# Uncomment and modify the line below based on your server setup
# chown -R www-data:www-data "$DB_DIR"
# OR for your specific user:
# chown -R your-username:your-groupname "$DB_DIR"

echo "Done! Now restart the service with: sudo systemctl restart calculators-server"
