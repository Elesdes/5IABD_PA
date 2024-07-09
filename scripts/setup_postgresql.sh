#!/bin/bash

# Function to install required packages
install_packages() {
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev libasound2
}

# Function to install PostgreSQL only
install_postgresql() {
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
}

# Function to run PostgreSQL commands
run_postgresql_commands() {
    sudo service postgresql start
    sudo -i -u postgres psql <<EOF
CREATE DATABASE icarus_db;
\c icarus_db
CREATE USER icarus WITH PASSWORD 'icarus';
GRANT ALL PRIVILEGES ON DATABASE icarus_db TO icarus;
EOF

    # Run the SQL script
    sudo -u postgres psql -d icarus_db -f create_tables.sql

    # Grant privileges
    sudo -i -u postgres psql -d icarus_db <<EOF
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO icarus;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO icarus;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO icarus;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO icarus;
EOF

    echo "PostgreSQL setup complete."
}

# Main logic to determine which actions to perform
if [ "$1" == "full" ]; then
    install_packages
    run_postgresql_commands
elif [ "$1" == "install" ]; then
    install_postgresql
elif [ "$1" == "setup" ]; then
    run_postgresql_commands
else
    echo "Usage: $0 {full|install|setup}"
    exit 1
fi
