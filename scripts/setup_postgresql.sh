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
    sudo -i -u postgres psql << EOF
CREATE DATABASE icarus_db;
\c icarus_db
CREATE USER icarus WITH PASSWORD 'icarus';
GRANT ALL PRIVILEGES ON DATABASE icarus_db TO icarus;

-- Create tables
CREATE TABLE IF NOT EXISTS USERS
(
    IdUser VARCHAR(64) NOT NULL PRIMARY KEY,
    Email VARCHAR(255) NOT NULL,
    Name VARCHAR(255) NOT NULL,
    Forename VARCHAR(255) NOT NULL,
    Password CHAR(255) NOT NULL,
    Cookie VARCHAR(255),
    Role INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MODELS
(
    IdModel SERIAL NOT NULL PRIMARY KEY,
    Path VARCHAR(255) NOT NULL,
    Date TIMESTAMP NOT NULL,
    IdUser VARCHAR(64) REFERENCES USERS(IdUser)
);

CREATE TABLE IF NOT EXISTS DEVICES
(
    IdDevice VARCHAR(8) NOT NULL PRIMARY KEY,
    IdUser VARCHAR(64) REFERENCES USERS(IdUser)
);

-- Grant privileges
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
