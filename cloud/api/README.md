# Run API on Local

## Install PostgreSQL and the BDD

In order to connect the website to our BDD, you need to have either a cloud structure connected to it or a local installation. We will explain how to install PostgreSQL and how to feed the database and the structure.

### Windows

#### Download and install PostgreSQL

Go to the official website of PostgreSQL and download the latest app wizard.

[PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

Follow the instructions and don't tick off any choices.
You'll need to set a password to your admin profile. Please be cautious while choosing it.
Let anything by default.
You don't need Stack builder to install anything else.

#### Create the database

Open pgAdmin4. Click on "Servers" in the left list. Write your password previously set.
Right click Login/Group Roles -> Create -> Login/Group Roles. Create your user. Please be careful, you'll need to accept "Can login?" Privileges.
Click on "Object" -> Create -> Database... Name your database and set your user as the owner.
Click on your newly created database. On the top left of the app, click Query Tool.
Copy and paste to query tool and execute the file : `cloud/sql/create_database_postgresql.sql`

### Linux (Ubuntu)

#### Download and install PostgreSQL

First, run these commands :
```bash
sudo apt-get update
sudo apt install postgresql postgresql-contrib libgconf-2-4 libatk1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libgbm-dev libnss3-dev libxss-dev libasound2
```

Then, run this :
```bash
sudo service postgresql start
sudo -i -u postgres
```

Then, run this :
```bash
psql
```

Lastly, run this :
```sql
CREATE DATABASE icarus_db;

CREATE TABLE IF NOT EXISTS USERS(
    IdUsers SERIAL NOT NULL PRIMARY KEY,
	Email VARCHAR(255) NOT NULL,
	Name VARCHAR(255) NOT NULL,
	Forename VARCHAR(255) NOT NULL,
    password CHAR(255) NOT NULL,
    Cookie VARCHAR(255),
	Role INT NOT NULL
);

CREATE TABLE IF NOT EXISTS MODEL
(
    IdModel SERIAL NOT NULL PRIMARY KEY,
	Path VARCHAR(255) NOT NULL,
	Date TIMESTAMP NOT NULL,
	IdUsers SERIAL REFERENCES USERS(IdUsers)
);
```

## Install Requirements

Run the following command in the `cloud` directory to install the required packages:

```bash
pip install -r requirements.txt
```

## Launch the API

Run script `cloud/api/src/main.py` to launch the API.