# Run API on Local

## Install PostgreSQL and the BDD

In order to connect the website to our BDD, you need to have either a cloud structure connected to it or a local installation. We will explain how to install PostgreSQL and how to feed the database and the structure.

### Windows

#### Setup & Run PostgreSQL

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
Copy and paste to query tool and execute the file : `scripts/create_database_postgresql.sql`

### Linux (Ubuntu)

For a full install (installing PostgreSQL and setup the database):

```bash
sudo apt install dos2unix
```

```bash
dos2unix scripts/setup_postgresql.sh
```

```bash
bash scripts/setup_postgresql.sh full
```

To install only PostgreSQL:

```bash
bash scripts/setup_postgresql.sh install
```

To only setup the database:

```bash
bash scripts/setup_postgresql.sh setup
```

## Install Requirements

```bash
pip install -r cloud/requirements.txt
```

## Launch the API

Run script `cloud/api/src/main.py` to launch the API.
